// Drives the admin console's Pages tab end to end against the LOCAL stack.
// Run:  lovemesomecoding_backend/scripts/run-local.sh   (:8099, `local` content tree)
//       (cd lovemesomecoding_frontend && npm run dev)   (:3000)
//       ADMIN_PASSWORD=... node projects/admin_pages/verify_admin_pages.mjs
//
// Writes go to s3://…/lovemesomecoding/local/ only. The script checks prod is untouched and
// restores the local About Me page from prod when it is done.
import { chromium } from 'playwright';
import { execFileSync } from 'child_process';
import path from 'path';

const BASE = process.env.BASE ?? 'http://localhost:3000';
const BUCKET = 's3://lovemesomecoding-db-329580012644-us-west-2-an/lovemesomecoding';
const shots = path.join(path.dirname(new URL(import.meta.url).pathname), 'screenshots');
const s3 = (tree) =>
  JSON.parse(execFileSync('aws', ['s3', 'cp', `${BUCKET}/${tree}/pages/about-me.json`, '-', '--profile', 'folau']));

const failures = [];
const check = (ok, msg) => { console.log(`  ${ok ? '✓' : '✗'} ${msg}`); if (!ok) failures.push(msg); };

const prodBefore = s3('prod');
const marker = `Playwright edit ${Date.now()}`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));

try {
  await page.goto(`${BASE}/admin`);
  await page.getByLabel(/username/i).fill('folauk');
  await page.getByLabel(/password/i).fill(process.env.ADMIN_PASSWORD ?? 'folaulisa1');
  await page.getByRole('button', { name: /sign in/i }).click();
  await page.getByRole('button', { name: 'Pages', exact: true }).click();

  const rows = page.locator('.post-row');
  await rows.first().waitFor();
  check((await rows.count()) === 12, `Pages tab lists 12 pages (${await rows.count()})`);
  await page.screenshot({ path: `${shots}/01-pages-list.png` });

  await page.locator('.post-row', { hasText: 'About Me' }).click();
  await page.getByLabel('Title').waitFor();
  check((await page.getByLabel('Title').inputValue()) === 'About Me', 'About Me loads into the editor');
  check(await page.getByText('this page carries layout markup from WordPress').isVisible(),
    'visual tab warns about the about-hero wrapper markup');
  check((await page.locator('.admin-card a[href="/about-me"]').count()) === 1, 'shows the fixed live URL');
  await page.screenshot({ path: `${shots}/02-about-me-visual.png` });

  await page.getByRole('button', { name: 'HTML', exact: true }).click();
  const textarea = page.locator('textarea');
  const originalHtml = await textarea.inputValue();
  check(originalHtml === prodBefore.contentHtml, 'HTML tab shows the stored body byte-for-byte');
  await textarea.fill(`${originalHtml}\n<p>${marker}</p>`);
  await page.getByRole('button', { name: 'Preview', exact: true }).click();
  check(await page.locator('.preview').getByText(marker).isVisible(), 'preview renders the edit');
  await page.screenshot({ path: `${shots}/03-about-me-preview.png` });

  await page.getByRole('button', { name: 'Save', exact: true }).click();
  await page.getByText('Saved. It goes live on the site after Publish site.').waitFor();
  await page.screenshot({ path: `${shots}/04-saved.png` });

  const local = s3('local');
  check(local.contentHtml.includes(marker), 'edit landed in the local content tree');
  check(local.contentHtml.includes('<div class="about-hero">'), 'wrapper markup survived the save (HTML tab)');
  check(local.url === '/about-me' && local.date === prodBefore.date, 'url and date unchanged');
  check(local.updatedBy === 'folauk', 'updatedBy recorded');
  const prodAfter = s3('prod');
  check(JSON.stringify(prodAfter) === JSON.stringify(prodBefore), 'prod About Me untouched');

  // The post editor now uses the same extracted BodyEditor — make sure it still works.
  await page.getByRole('button', { name: 'Back to posts' }).click();
  await page.locator('.post-row').first().click();
  await page.getByRole('button', { name: 'HTML', exact: true }).click();
  check((await page.locator('textarea').inputValue()).length > 0, 'post editor still loads a body into the HTML tab');
  check(await page.getByRole('button', { name: 'Save & publish' }).isVisible(), 'post editor still has its own actions');
  await page.screenshot({ path: `${shots}/05-post-editor.png` });

  check(errors.length === 0, `no page errors (${errors.join('; ')})`);
} finally {
  await browser.close();
  // Put the local tree back the way the seed left it.
  execFileSync('aws', ['s3', 'cp', `${BUCKET}/prod/pages/about-me.json`, `${BUCKET}/local/pages/about-me.json`,
    '--profile', 'folau', '--only-show-errors']);
}

if (failures.length) { console.error(`\n${failures.length} failed`); process.exit(1); }
console.log('\nall admin page checks passed');
