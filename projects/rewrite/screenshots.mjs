// Visual check of the built site against the preview server.
// Run:  node scripts/preview.mjs &   then   node projects/rewrite/screenshots.mjs
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const BASE = process.env.BASE ?? 'http://localhost:4321';
const outDir = path.join(path.dirname(new URL(import.meta.url).pathname), 'screenshots');
fs.mkdirSync(outDir, { recursive: true });

const SHOTS = [
  { name: '01-home', url: '/', full: false },
  { name: '02-category-java8', url: '/java-8', full: false },
  { name: '03-post-top', url: '/java-8/java-25-migration-guide', full: false },
  { name: '04-post-code', url: '/java-8/java-25-migration-guide', scrollTo: 2400 },
  { name: '05-post-dark', url: '/java-8/java-25-migration-guide', theme: 'dark', scrollTo: 2400 },
  { name: '06-home-dark', url: '/', theme: 'dark' },
  { name: '07-mobile-home', url: '/', viewport: { width: 390, height: 844 } },
  { name: '08-mobile-post', url: '/java-8/java-25-migration-guide', viewport: { width: 390, height: 844 }, scrollTo: 1200 },
  { name: '09-404', url: '/this-page-is-gone' },
  { name: '10-page-about', url: '/about-me' },
];

const browser = await chromium.launch();
const errors = [];

for (const shot of SHOTS) {
  const context = await browser.newContext({
    viewport: shot.viewport ?? { width: 1440, height: 900 },
    deviceScaleFactor: 2,
  });
  if (shot.theme) {
    await context.addInitScript((t) => localStorage.setItem('theme', t), shot.theme);
  }
  const page = await context.newPage();

  page.on('pageerror', (e) => errors.push(`${shot.url}: ${e.message}`));
  page.on('console', (m) => {
    if (m.type() === 'error') errors.push(`${shot.url}: console ${m.text()}`);
  });

  const res = await page.goto(BASE + shot.url, { waitUntil: 'networkidle' });
  if (shot.scrollTo) {
    await page.evaluate((y) => window.scrollTo(0, y), shot.scrollTo);
    await page.waitForTimeout(300);
  }
  await page.screenshot({
    path: path.join(outDir, `${shot.name}.png`),
    fullPage: Boolean(shot.full),
  });
  console.log(`  ${shot.name.padEnd(18)} ${res.status()}  ${shot.url}`);
  await context.close();
}

/* ---- interaction checks ---- */
const context = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
const page = await context.newPage();

await page.goto(`${BASE}/`, { waitUntil: 'networkidle' });
await page.click('.search input');
await page.fill('.search input', 'stream gatherers');
await page.waitForSelector('.search-results a', { timeout: 5000 });
const hits = await page.locator('.search-results a .r-title').allTextContents();
await page.screenshot({ path: path.join(outDir, '11-search.png') });
console.log(`  search             ${hits.length} hits, first: ${hits[0]}`);

await page.goto(`${BASE}/java-8/java-25-migration-guide`, { waitUntil: 'networkidle' });
await page.hover('.code-wrap');
await page.click('.code-wrap .code-copy');
await page.waitForTimeout(300);
const label = await page.locator('.code-wrap .code-copy').first().textContent();
console.log(`  copy button        -> "${label}"`);

await page.locator('.nav-group button').first().hover();
await page.waitForSelector('.nav-dropdown a', { timeout: 3000 });
await page.screenshot({ path: path.join(outDir, '12-nav-dropdown.png') });
console.log(`  nav dropdown       ok`);

await context.close();
await browser.close();

console.log(`\nscreenshots -> ${outDir}`);
if (errors.length) {
  console.log('\nJS errors:');
  for (const e of [...new Set(errors)]) console.log(`  ${e}`);
} else {
  console.log('no console/page errors');
}
