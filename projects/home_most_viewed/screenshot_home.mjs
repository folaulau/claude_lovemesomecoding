import { chromium } from 'playwright';
const S = process.argv[2];
const b = await chromium.launch();
for (const [name, vp, scheme] of [['desktop',{width:1280,height:1100},'light'],['mobile',{width:390,height:1400},'light'],['dark',{width:1280,height:1100},'dark']]) {
  const p = await b.newPage({ viewport: vp, colorScheme: scheme });
  await p.goto('http://localhost:4321/');
  await p.locator('#most-viewed-heading').scrollIntoViewIfNeeded();
  await p.evaluate(() => window.scrollTo(0, document.querySelector('#most-viewed-heading').getBoundingClientRect().top + scrollY - 80));
  const cards = await p.locator('.mv-card').count();
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  console.log(name, 'cards', cards, 'hscroll', overflow);
  await p.screenshot({ path: `${S}/home-${name}.png` });
}
await b.close();
