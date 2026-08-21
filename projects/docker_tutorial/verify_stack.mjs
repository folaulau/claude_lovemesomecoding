/**
 * Prove the containerised stack actually works in a browser.
 *
 * curl can show that nginx returns 200 for /menu and proxies /api — it cannot show that the
 * single-page app boots, that its JavaScript reaches the API, or that products render. Those are
 * the things that break when `fileReplacements`, a build arg or a proxy_pass is wrong, and they
 * all still return 200.
 *
 * Run the stack first:
 *   cd lovemesomecoding_demo_project/pizza && docker compose --profile angular up -d --build
 *
 * Then:
 *   node projects/docker_tutorial/verify_stack.mjs
 *
 * Uses the Playwright already installed in pizza-react-frontend rather than adding a dependency.
 */

import { chromium } from '../../lovemesomecoding_demo_project/pizza/pizza-react-frontend/node_modules/playwright/index.mjs';

const TARGETS = [
  { name: 'React   (web)',         url: 'http://localhost:8080' },
  { name: 'Angular (web-angular)', url: 'http://localhost:4201' },
];

const failures = [];

const browser = await chromium.launch();

for (const target of TARGETS) {
  const context = await browser.newContext();
  const page = await context.newPage();

  // Every request the page makes, so we can prove the API calls went to the SPA's own origin
  // rather than to an absolute http://localhost:8085 baked into the bundle.
  const apiCalls = [];
  page.on('request', (r) => {
    if (r.url().includes('/api/')) apiCalls.push(r.url());
  });
  const consoleErrors = [];
  page.on('console', (m) => m.type() === 'error' && consoleErrors.push(m.text()));
  page.on('pageerror', (e) => consoleErrors.push(String(e)));

  try {
    // A deep link, not the root — this only works if nginx's try_files fallback is right.
    await page.goto(`${target.url}/menu`, { waitUntil: 'networkidle', timeout: 30_000 });

    // The menu renders one card per product. If the API call failed, the page still loads and
    // this is 0 — which is exactly the failure mode a 200 from curl hides.
    const cards = await page.locator('.card').count();
    const title = await page.title();

    const sameOrigin = apiCalls.every((u) => u.startsWith(target.url));

    const ok = cards > 0 && apiCalls.length > 0 && sameOrigin && consoleErrors.length === 0;
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${target.name}`);
    console.log(`        title          ${title}`);
    console.log(`        product cards  ${cards}`);
    console.log(`        /api/ requests ${apiCalls.length}, all same-origin: ${sameOrigin}`);
    if (apiCalls.length) console.log(`        first          ${apiCalls[0]}`);
    if (consoleErrors.length) {
      console.log(`        console errors ${consoleErrors.length}`);
      consoleErrors.slice(0, 3).forEach((e) => console.log(`          ! ${e.slice(0, 160)}`));
    }
    if (!ok) failures.push(target.name);
  } catch (err) {
    console.log(`FAIL  ${target.name}: ${err.message.split('\n')[0]}`);
    failures.push(target.name);
  }

  await context.close();
}

await browser.close();

if (failures.length) {
  console.log(`\n${failures.length} target(s) failed: ${failures.join(', ')}`);
  process.exit(1);
}
console.log('\nboth containerised frontends boot, reach the API on their own origin, and render products');
