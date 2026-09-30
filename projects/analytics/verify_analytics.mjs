// End-to-end check of the GA4 wiring against the built site.
// Run:  (cd lovemesomecoding_frontend && npm run build && node scripts/preview.mjs &)
//       node projects/analytics/verify_analytics.mjs
//
// lovemesomecoding.com is mapped onto the local preview so the hostname guard passes,
// and every Google request is intercepted and aborted — recorded, never sent to GA.
// BASE=https://lovemesomecoding.com runs it against the live site instead (hits are
// still aborted, so it never pollutes the numbers).
import { chromium } from 'playwright';

const LIVE = !!process.env.BASE;
const BASE = process.env.BASE ?? 'http://lovemesomecoding.com';
const GA_ID = 'G-ETM6754MYL';

const browser = await chromium.launch({
  args: LIVE ? [] : ['--host-resolver-rules=MAP lovemesomecoding.com 127.0.0.1:4321'],
});
const failures = [];
const check = (ok, msg) => { console.log(`  ${ok ? '✓' : '✗'} ${msg}`); if (!ok) failures.push(msg); };

async function visit(url, act) {
  const page = await browser.newPage({ permissions: ['clipboard-read', 'clipboard-write'] });
  // The mapped origin is plain http — not a secure context, so navigator.clipboard does not
  // exist (and headless ignores --unsafely-treat-insecure-origin-as-secure). Stub it.
  if (!LIVE) await page.addInitScript(() => {
    if (!navigator.clipboard) Object.defineProperty(navigator, 'clipboard', { value: { writeText: async () => {} } });
  });
  const hits = [];
  await page.route(/googletagmanager\.com|google-analytics\.com/, (route) => {
    hits.push(route.request().url());
    // Serve a stub gtag.js so the page behaves as if Google answered, without contacting it.
    if (route.request().url().includes('/gtag/js')) return route.fulfill({ contentType: 'text/javascript', body: '' });
    return route.abort();
  });
  await page.goto(BASE + url, { waitUntil: 'networkidle' });
  const result = act ? await act(page) : undefined;
  const dataLayer = await page.evaluate(() => (window.dataLayer ?? []).map((a) => Array.from(a)));
  await page.close();
  return { hits, dataLayer, result };
}

const events = (dl, name) => dl.filter((a) => a[0] === 'event' && a[1] === name);

console.log(`verify analytics against ${BASE}`);

const home = await visit('/');
check(home.hits.some((u) => u.includes(`gtag/js?id=${GA_ID}`)), 'home loads gtag.js with the measurement id');
check(home.dataLayer.some((a) => a[0] === 'config' && a[1] === GA_ID), 'home configures GA');

const post = await visit('/java-8/java-25-migration-guide', async (page) => {
  await page.locator('[data-copy]').first().click();
  await page.waitForTimeout(300);
  return { label: await page.locator('[data-copy]').first().textContent(), path: new URL(page.url()).pathname };
});
check(post.hits.some((u) => u.includes('gtag/js')), 'post page loads gtag.js');
check(post.result.label === 'Copied', `copy button still copies (label: ${post.result.label})`);
const copies = events(post.dataLayer, 'code_copy');
check(copies.length === 1, `one code_copy event (${JSON.stringify(copies[0]?.[2])})`);
check(copies[0]?.[2]?.page_path === post.result.path && copies[0]?.[2]?.language !== 'unknown',
  'code_copy carries page_path and language');

const admin = await visit('/admin');
check(admin.hits.length === 0, `/admin makes no Google request (${admin.hits.length})`);
check(admin.dataLayer.length === 0, '/admin never touches dataLayer');

if (!LIVE) {
  const page = await browser.newPage();
  const hits = [];
  await page.route(/googletagmanager\.com/, (r) => { hits.push(r.request().url()); return r.abort(); });
  await page.goto('http://localhost:4321/', { waitUntil: 'networkidle' });
  await page.close();
  check(hits.length === 0, `localhost preview sends nothing (${hits.length})`);
}

await browser.close();
if (failures.length) { console.error(`\n${failures.length} failed`); process.exit(1); }
console.log('\nall analytics checks passed');
