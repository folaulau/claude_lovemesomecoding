# Session 08-step6-tests

mode: `acceptEdits`  cwd: `/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza`  allowed: `Bash(npm run:*) Bash(npx playwright:*) Bash(npx tsc:*) Bash(git diff:*) Bash(git status:*) Bash(curl:*)`  resumed: `aa622bee-305d-4a91-bbfa-0b046bb02d30`

## Prompt

```text
Step 5 committed as 34784b02, with your fieldset fix. I checked it in a real browser at 1280 and 390px and asserted getByRole('group', { name: 'Pay with' }).

Implement STEP 6 ONLY (e2e/saved-card-checkout.spec.ts + add it to test:e2e), as planned. The app is still running with Stripe test keys. Requirements beyond the plan:
- Each test must fail if the behaviour it names is broken. For at least two tests, prove it: temporarily break the code they cover, show me the failure, and restore it.
- Clean up everything the tests create (saved cards; note any orders you can't remove).
Run the new spec and npm run test:all. Don't commit. Summarise.
```

## Transcript

Starting step 6. I'll check how the cart is stored, the Playwright config, and the `test:e2e` script first, so the spec can clean up after itself.

- **Bash** command='git log --oneline -1 && git status --short && grep -n "Mapping\\|@Operation(summary" pizza-springboot-backend/src/main/java/com/pizza/api/entity/cart/CartRestController.java | head -20 && grep -n "cart'
- **Write** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/e2e/saved-card-checkout.spec.ts'
- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend && npx playwright test e2e/saved-card-checkout.spec.ts --reporter=line 2>&1 | grep -vE "'
Six pass. The 3D Secure test, which I added beyond the plan, failed: after "Complete" was clicked the page stayed on `/checkout`. Checking the page snapshot for what happened:

- **Bash** command='grep -n -i "alert\\|declin\\|authenticat\\|complete\\|iframe\\|Processing" "test-results/saved-card-checkout-paying-e97f1-ompleting-it-pays-the-order-chromium/error-context.md" | head -20'
- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/e2e/saved-card-checkout.spec.ts'
- **Bash** command='npx playwright test e2e/saved-card-checkout.spec.ts --reporter=line --repeat-each=3 -g "3D Secure" 2>&1 | grep -vE "^\\s+at |node_modules" | tail -15'
3 of 3 pass now. Running the whole spec once more before the break-it proofs:

- **Bash** command='npx playwright test e2e/saved-card-checkout.spec.ts --reporter=line 2>&1 | tail -3'
7 of 7 pass. **Proof 1:** I'll break the expiry rule so `isCardExpired` always returns `false`, then run the expired-card test:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/src/lib/cards.ts'
- **Bash** command='sleep 2; npx playwright test e2e/saved-card-checkout.spec.ts --reporter=line -g "expired card" 2>&1 | grep -vE "^\\s+at |node_modules" | sed -n 1,25p'
The test fails as it should: the expired card was enabled, and it was even preselected (`checked`). Restoring:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/src/lib/cards.ts'
**Proof 2:** I'll break the decline handling so that a Stripe error is treated as success (`onSuccess()` instead of showing the message), then run the decline test:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/src/components/SavedCardPayment.tsx'
- **Bash** command='sleep 2; npx playwright test e2e/saved-card-checkout.spec.ts --reporter=line -g "declined" 2>&1 | grep -vE "^\\s+at |node_modules" | sed -n 1,25p'
The test fails as it should: no decline message appeared, because the broken code navigated away as if the payment had succeeded. Restoring:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/src/components/SavedCardPayment.tsx'
**Proof 3:** the guest test has the weakest-looking assertion, so I'm proving it too. I'll remove the `isAuthenticated` guard on the card load in `CheckoutPage`:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/src/pages/CheckoutPage.tsx'
- **Bash** command='sleep 2; npx playwright test e2e/saved-card-checkout.spec.ts --reporter=line -g "guest never" 2>&1 | grep -vE "^\\s+at |node_modules" | sed -n 1,22p'
The test fails as it should: the guest got the chooser (and its "Pay … with Visa" button) in place of the plain card form. Restoring:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/src/pages/CheckoutPage.tsx'
- **Bash** command='git status --short && git diff --stat && grep -rn "TEMP BREAK" src e2e; echo "temp-break markers: $(grep -rc \'TEMP BREAK\' src | grep -v \':0\' | wc -l)"'
- **Bash** command='git status --short'
- **Bash** command='grep -rn "TEMP BREAK" src e2e'
All three breaks are restored: `src/` matches the commit exactly and only the new spec is untracked. Now adding the spec to `test:e2e`:

- **Read** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/package.json'
- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/package.json'
- **Bash** command='npm run typecheck 2>&1 | tail -3'
- **Bash** command='npx oxlint e2e/saved-card-checkout.spec.ts'
- **Bash** command='npm run lint 2>&1 | grep -E "saved-card|error|Found" ; echo done'
Lint reports nothing for the new spec. Now `npm run test:all`, with nothing else running against the backend:

- **Bash** command='npm run test:all -- --reporter=line 2>&1 | grep -vE "^\\s+at |node_modules|^\\[[0-9]+/[0-9]+\\]" | tail -50'
- **Bash** command='grep -n -i "revenue\\|orders\\|no data\\|no orders\\|last\\|days\\|\\\\$" "test-results/admin-reports-dashboard-renders-tiles-and-both-charts-chromium/error-context.md" | head -30'
- **Read** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/test-results/admin-reports-dashboard-renders-tiles-and-both-charts-chromium/error-context.m'
- **Read** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/test-results/admin-reports-dashboard-renders-tiles-and-both-charts-chromium/error-context.m'
- **Bash** command='TOKEN=$(curl -s -X POST http://localhost:8085/api/auth/login -H \'Content-Type: application/json\' -d \'{"email":"customer@pizza.test","password":"pizza123"}\' | sed -E \'s/.*"token":"([^"]+)".*/\\1/\'); cur'
- **Bash** command='git status --short && git diff'
Step 6 is in place: the new spec passes 7 of 7, and three temporarily broken pieces of code each made the matching test fail. `npm run test:all` gives 103 passed, 2 failed and 2 skipped. The 2 failures are `admin.spec.ts` report-chart tests that this ticket's changes don't touch. Nothing is committed.

## What changed
- **New `e2e/saved-card-checkout.spec.ts`, 7 tests.**
  - With a faked card list (no Stripe needed):
    - The **primary** card is preselected and named on the Pay button. The primary is deliberately not first in the list, so "first card" and "primary card" disagree.
    - An expired card is shown, disabled, labelled "Expired" and never preselected. The expired card is the primary, so a naive "preselect the primary" would pick it.
    - "Use a new card" swaps in the ordinary card form.
    - A guest never sees the chooser, and the card list is never even requested.
  - Live, against Stripe test mode:
    - A saved card pays the order, and our API reports PAID with `visa` and `4242`.
    - A declined card shows the decline, the order stays waiting for payment, and a second saved card pays the same order (the API reports 4242, not 0341).
    - A card that needs 3D Secure shows Stripe's challenge, completing it pays the order, and the API reports `3184`.
  - All chooser checks find the group by its accessible name, `getByRole('group', { name: 'Pay with' })`.
- **`package.json`:** `saved-card-checkout.spec.ts` added to `test:e2e`.

## Proof that tests fail when the behaviour breaks
Each break was restored straight after; `src/` now matches commit `34784b02` exactly.

| Temporary break | Test | Failure |
|---|---|---|
| `isCardExpired` always returns `false` (`lib/cards.ts`) | expired card | `toBeDisabled` failed: the expired card was enabled and even preselected |
| A Stripe decline calls `onSuccess()` (`SavedCardPayment.tsx`) | declined card | the decline message never appeared |
| Card load runs for guests (`CheckoutPage.tsx`) | guest | the plain card form never appeared; the chooser showed instead |

## Results
- **`saved-card-checkout.spec.ts`:** 7 of 7, twice. The 3D Secure test also passed 3 out of 3 when run alone.
- **`npm run test:all`:** 103 passed, 2 failed, 2 skipped.
  - **The 2 failures** are both in `admin.spec.ts`: the revenue line chart is never drawn. The 30-day report window contains only today's orders, all from test runs, because the seeded orders are from August. A line needs at least two days of data. Before today's runs the window had zero orders, so these tests couldn't pass then either. It's the same stale-seed-date problem as the 4 backend report tests, and nothing in this ticket touches reports.
  - **The 2 skipped tests** are not from this spec. If its live Stripe tests had been skipped there would be at least three.
- **typecheck and lint:** clean.

## Cleanup
- **Saved cards:** every card a test saves is deleted in `afterEach` (which also removes it from the Stripe customer), and the test fails if a delete doesn't return 204. That cleanup also ran in the deliberately broken runs. I couldn't list the cards directly afterwards because the command needed an approval I didn't have.
- **Orders I can't remove:** there's no API to delete an order, and cancelling them would only skew a different count. Each run of this spec leaves 7 orders: 4 waiting for payment (one of them a guest's) and 3 PAID. With every run today, that's about 27 orders from step 6, on top of the ones from step 5. They're all part of why today is the only day in the report window.

## Differences from the plan
1. **Results are checked through our API, not SQL.** `payment-status` reads the order back from our database. Running `mysql` needed an approval I didn't have.
2. **Two tests the plan didn't list:** "Use a new card", and 3D Secure, which the plan had left as manual. It turned out to be automatable. It retries the "Complete" click, because Stripe's test page ignores a click that comes too early. Drop it if you'd rather not depend on Stripe's test page.
3. **Cleanup removes only the cards the test created,** not every card on the demo customer, so cards saved by hand survive. The live tests pick their card explicitly so a leftover primary can't interfere.
4. **Skip detection:** the live tests skip if the backend can't open a SetupIntent. That opens one test-mode SetupIntent per run, but stores nothing on our side.

The one plan check still not automated is **decline, then a typed new card on the same order**: an automated browser can't type into Stripe's card form.


_turns: 31, duration: 643s, cost: $8.82_

## Final answer

Step 6 is in place: the new spec passes 7 of 7, and three temporarily broken pieces of code each made the matching test fail. `npm run test:all` gives 103 passed, 2 failed and 2 skipped. The 2 failures are `admin.spec.ts` report-chart tests that this ticket's changes don't touch. Nothing is committed.

## What changed
- **New `e2e/saved-card-checkout.spec.ts`, 7 tests.**
  - With a faked card list (no Stripe needed):
    - The **primary** card is preselected and named on the Pay button. The primary is deliberately not first in the list, so "first card" and "primary card" disagree.
    - An expired card is shown, disabled, labelled "Expired" and never preselected. The expired card is the primary, so a naive "preselect the primary" would pick it.
    - "Use a new card" swaps in the ordinary card form.
    - A guest never sees the chooser, and the card list is never even requested.
  - Live, against Stripe test mode:
    - A saved card pays the order, and our API reports PAID with `visa` and `4242`.
    - A declined card shows the decline, the order stays waiting for payment, and a second saved card pays the same order (the API reports 4242, not 0341).
    - A card that needs 3D Secure shows Stripe's challenge, completing it pays the order, and the API reports `3184`.
  - All chooser checks find the group by its accessible name, `getByRole('group', { name: 'Pay with' })`.
- **`package.json`:** `saved-card-checkout.spec.ts` added to `test:e2e`.

## Proof that tests fail when the behaviour breaks
Each break was restored straight after; `src/` now matches commit `34784b02` exactly.

| Temporary break | Test | Failure |
|---|---|---|
| `isCardExpired` always returns `false` (`lib/cards.ts`) | expired card | `toBeDisabled` failed: the expired card was enabled and even preselected |
| A Stripe decline calls `onSuccess()` (`SavedCardPayment.tsx`) | declined card | the decline message never appeared |
| Card load runs for guests (`CheckoutPage.tsx`) | guest | the plain card form never appeared; the chooser showed instead |

## Results
- **`saved-card-checkout.spec.ts`:** 7 of 7, twice. The 3D Secure test also passed 3 out of 3 when run alone.
- **`npm run test:all`:** 103 passed, 2 failed, 2 skipped.
  - **The 2 failures** are both in `admin.spec.ts`: the revenue line chart is never drawn. The 30-day report window contains only today's orders, all from test runs, because the seeded orders are from August. A line needs at least two days of data. Before today's runs the window had zero orders, so these tests couldn't pass then either. It's the same stale-seed-date problem as the 4 backend report tests, and nothing in this ticket touches reports.
  - **The 2 skipped tests** are not from this spec. If its live Stripe tests had been skipped there would be at least three.
- **typecheck and lint:** clean.

## Cleanup
- **Saved cards:** every card a test saves is deleted in `afterEach` (which also removes it from the Stripe customer), and the test fails if a delete doesn't return 204. That cleanup also ran in the deliberately broken runs. I couldn't list the cards directly afterwards because the command needed an approval I didn't have.
- **Orders I can't remove:** there's no API to delete an order, and cancelling them would only skew a different count. Each run of this spec leaves 7 orders: 4 waiting for payment (one of them a guest's) and 3 PAID. With every run today, that's about 27 orders from step 6, on top of the ones from step 5. They're all part of why today is the only day in the report window.

## Differences from the plan
1. **Results are checked through our API, not SQL.** `payment-status` reads the order back from our database. Running `mysql` needed an approval I didn't have.
2. **Two tests the plan didn't list:** "Use a new card", and 3D Secure, which the plan had left as manual. It turned out to be automatable. It retries the "Complete" click, because Stripe's test page ignores a click that comes too early. Drop it if you'd rather not depend on Stripe's test page.
3. **Cleanup removes only the cards the test created,** not every card on the demo customer, so cards saved by hand survive. The live tests pick their card explicitly so a leftover primary can't interfere.
4. **Skip detection:** the live tests skip if the backend can't open a SetupIntent. That opens one test-mode SetupIntent per run, but stores nothing on our side.

The one plan check still not automated is **decline, then a typed new card on the same order**: an automated browser can't type into Stripe's card form.
