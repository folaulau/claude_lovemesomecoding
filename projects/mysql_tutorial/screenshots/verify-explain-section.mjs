import { chromium } from '/Users/folaukaveinga/Github/claude_lovemesomecoding/node_modules/playwright/index.mjs';

const URL = 'http://localhost:3000/sql/mysql-interview-advanced-queries';
const OUT = '/Users/folaukaveinga/Github/claude_lovemesomecoding/projects/mysql_tutorial/screenshots';

const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1280, height: 1000 } });
await p.goto(URL, { waitUntil: 'networkidle' });

// The new section
const h = await p.locator('h2', { hasText: 'This query is slow' }).first();
await h.scrollIntoViewIfNeeded();
await p.waitForTimeout(400);
await p.screenshot({ path: `${OUT}/explain-01-section-top.png` });

// how many code blocks highlighted?
const langs = await p.$$eval('pre code', els => els.map(e => e.className));
console.log('code blocks:', langs.length);
console.log('unhighlighted:', langs.filter(c => !/language-/.test(c)).length);
const tokens = await p.$$eval('pre code.language-sql .token', els => els.length);
console.log('sql prism tokens:', tokens);

// toc entries
const toc = await p.$$eval('nav a, aside a', els => els.map(e => e.textContent.trim()).filter(t => /slow|Step|does not go/i.test(t)));
console.log('toc:', toc);

// horizontal overflow on the plan blocks?
const over = await p.$$eval('pre', els => els.map(e => ({w: e.scrollWidth, c: e.clientWidth})).filter(o => o.w > o.c).length);
console.log('pre blocks that scroll horizontally:', over, 'of', (await p.$$('pre')).length);

for (const [i, sel] of [['02', 'Step 2 —'], ['03', 'Step 3 —'], ['04', 'Step 4 —'], ['05', 'What does not go away']]) {
  const el = p.locator('h3', { hasText: sel }).first();
  if (await el.count()) {
    await el.scrollIntoViewIfNeeded();
    await p.waitForTimeout(300);
    await p.screenshot({ path: `${OUT}/explain-${i}.png` });
  }
}
await b.close();
