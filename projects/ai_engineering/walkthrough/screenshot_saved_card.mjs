// Screenshots of PIZZA-42's card chooser, for the walkthrough post and the PR.
//
// Needs the pizza backend on :8085 and the React dev server on :5173. Saves two test cards to
// customer@pizza.test through our own API (one good, one that declines when charged), walks to the
// payment step, screenshots it at desktop and phone width, then deletes the cards again.
//
//   node projects/ai_engineering/walkthrough/screenshot_saved_card.mjs

import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const WEB = path.resolve(HERE, '../../../lovemesomecoding_demo_project/pizza/pizza-react-frontend');
const { chromium } = createRequire(path.join(WEB, 'package.json'))('@playwright/test');

const API = 'http://localhost:8085';
const APP = 'http://localhost:5173';

async function api(method, url, token, body) {
  const res = await fetch(API + url, {
    method,
    headers: { 'Content-Type': 'application/json', ...(token && { Authorization: `Bearer ${token}` }) },
    body: body && JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`${method} ${url} -> ${res.status} ${await res.text()}`);
  return res.status === 204 ? null : res.json();
}

const login = await api('POST', '/api/auth/login', null, { email: 'customer@pizza.test', password: 'pizza123' });
const token = login.token ?? login.accessToken;
const saved = [];
for (const pm of ['pm_card_visa', 'pm_card_chargeCustomerFail']) {
  saved.push(await api('POST', '/api/me/payment-methods', token, { stripePaymentMethodId: pm }));
}

const browser = await chromium.launch();
try {
  for (const [name, viewport] of [['desktop', { width: 1280, height: 900 }], ['mobile', { width: 390, height: 844 }]]) {
    const page = await browser.newPage({ viewport });
    await page.goto(`${APP}/login`);
    await page.getByLabel('Email').fill('customer@pizza.test');
    await page.getByLabel('Password').fill('pizza123');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await page.waitForURL((url) => !url.pathname.startsWith('/login'));

    await page.goto(`${APP}/menu?type=PIZZA`);
    await page.getByRole('heading', { name: 'Pepperoni Pizza', exact: true })
      .locator('xpath=ancestor::div[contains(@class,"product-card")]')
      .getByRole('button', { name: 'Build it' }).click();
    // The cart syncs to the server after the click; leaving before that write lands loses it.
    const synced = page.waitForResponse((r) => /\/api\/carts/.test(r.url()) && r.request().method() !== 'GET');
    await page.getByRole('dialog').getByRole('button', { name: 'Add to cart' }).click();
    await synced;
    // The cart lives on the server, so going straight to /checkout works at any width (on a phone
    // the cart button is inside the collapsed navbar).
    await page.getByRole('dialog').waitFor({ state: 'hidden' });
    await page.goto(`${APP}/checkout`);

    // Signed-in step 1 is prefilled from the profile; fill whatever is still empty.
    for (const [label, value] of [['Name', 'Demo Customer'], ['Email', 'customer@pizza.test'], ['Phone', '8015550100'], ['Street address', '123 Test St'],
      ['City', 'Salt Lake City'], ['State', 'UT'], ['ZIP', '84101']]) {
      const field = page.getByLabel(label, { exact: true });
      if (await field.count() && await field.isVisible() && !(await field.inputValue())) await field.fill(value);
    }
    await page.getByRole('button', { name: /Continue to payment/ }).click();
    await page.getByRole('button', { name: /^Pay .* with / }).waitFor({ timeout: 20000 })
      .catch(async (e) => { await page.screenshot({ path: path.join(HERE, `debug-${name}.png`), fullPage: true }); throw e; });
    // The radios must be one group with an accessible name, or a screen reader never says "Pay with".
    console.log(`${name}: group "Pay with" accessible name ->`, await page.getByRole('group', { name: 'Pay with' }).count());
    await page.screenshot({ path: path.join(HERE, `saved-card-chooser-${name}.png`), fullPage: true });
    console.log(`saved-card-chooser-${name}.png`);
    await page.close();
  }
} finally {
  await browser.close();
  for (const card of saved) await api('DELETE', `/api/me/payment-methods/${card.id}`, token);
}
