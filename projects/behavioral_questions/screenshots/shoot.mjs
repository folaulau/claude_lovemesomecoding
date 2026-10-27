// Screenshots of the Behavioral Questions track against the local dev server (:3000).
// Run from lovemesomecoding_frontend:  node ../projects/behavioral_questions/screenshots/shoot.mjs
import { chromium } from 'playwright';
const out = new URL('.', import.meta.url).pathname;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await page.goto('http://localhost:3000/behavioral-questions', { waitUntil: 'networkidle' });
await page.screenshot({ path: `${out}archive.png` });
await page.goto('http://localhost:3000/behavioral-questions/behavioral-proudest-project', { waitUntil: 'networkidle' });
await page.locator('blockquote').first().scrollIntoViewIfNeeded();
await page.screenshot({ path: `${out}proudest-project-answer.png` });
await browser.close();
