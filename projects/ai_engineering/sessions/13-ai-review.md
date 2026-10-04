# Session 13-ai-review

mode: `plan`  cwd: `/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza`

## Prompt

```text
You are reviewing a pull request you did not write. Branch feature/checkout-saved-cards against main in this repo (git diff main...feature/checkout-saved-cards; the PR touches pizza/pizza-springboot-backend and pizza/pizza-react-frontend). The PR description is at pizza/../../claude_lovemesomecoding/projects/ai_engineering/sessions/12-pr-body.md if you can read it; otherwise review the diff alone.

Review for correctness and security first: payment logic, authorization, race conditions, error handling, and whether the tests would catch a regression. Then anything that contradicts the project's CLAUDE.md rules.

Rules:
- Report only findings you are confident are real. For each: file:line, what is wrong, a concrete scenario where it breaks, and severity (blocker / should-fix / nit).
- Say explicitly if you looked for a class of bug and found nothing.
- Do not change any files.
```

## Transcript

- **Bash** command='git diff --stat main...feature/checkout-saved-cards && ls ../../projects/ai_engineering/sessions/ 2>/dev/null | head; cat ../../projects/ai_engineering/sessions/12-pr-body.md 2>/dev/null'
- **Bash** command='git diff main...feature/checkout-saved-cards -- pizza-springboot-backend/src/main pizza-react-frontend/src pizza-react-frontend/package.json'
- **Read** file_path='/Users/folaukaveinga/.claude-personal/projects/-Users-folaukaveinga-Github-claude-lovemesomecoding-lovemesomecoding-demo-project-pizza/92220511-ecf0-464e-a2ee-f55ea3d0d03e/tool-results/b35thndfm.txt'
- **Bash** command='git checkout -q 2>/dev/null; B=feature/checkout-saved-cards; R=pizza-springboot-backend/src/main/java/com/pizza/api; git show $B:pizza/$R/payment/StripeService.java | sed -n 60,260p; echo ----SEC; git'
- **Bash** command='B=feature/checkout-saved-cards; R=pizza-springboot-backend/src/main/java/com/pizza/api; git show $B:pizza/$R/entity/order/CustomerOrderServiceImpl.java | sed -n 40,200p; git show $B:pizza/$R/entity/or'
Reviewing the backend and frontend diff now; next I'm checking how the API client handles 204 responses and what the new tests actually assert.

- **Bash** command='B=feature/checkout-saved-cards; git show $B:pizza/pizza-react-frontend/src/lib/api.ts | grep -n -A12 -E "204|status ===|json\\(\\)|put" | head -60; grep -rn "UserPaymentMethodRepository\\b" pizza-springb'
- **Bash** command='git grep -n "UserPaymentMethodRepository\\|paymentMethodRepository\\." feature/checkout-saved-cards -- \'pizza-springboot-backend/src/main/*.java\' | grep -v "Repository.java:"; git grep -n "401\\|403\\|ano'
- **Bash** command='git show feature/checkout-saved-cards:pizza/pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/CustomerOrderSavedCardTest.java | sed -n 1,140p'
- **Bash** command='git diff main...feature/checkout-saved-cards -- CLAUDE.md; git show main:pizza/CLAUDE.md | grep -n "tests;" ; git grep -c "@Test" main -- pizza-springboot-backend/src/test | awk -F: \'{s+=$NF} END {pri'
- **Bash** command='git show feature/checkout-saved-cards:pizza/pizza-react-frontend/e2e/saved-card-checkout.spec.ts | sed -n 1,304p | grep -n -E "test\\(|skip|route\\(|afterEach|afterAll|delete|expect\\(.*PAID|confirm|fina'
- **Bash** command='git show feature/checkout-saved-cards:pizza/pizza-react-frontend/e2e/saved-card-checkout.spec.ts | sed -n 186,304p'
Main diff reviewed; now checking the branch's commits against the repo's git rules, then writing up the findings.

- **Bash** command='git log --format=\'%h %an <%ae>%n%b---\' main..feature/checkout-saved-cards | grep -iE "^[0-9a-f]{7,} |co-authored|^---" ; git diff --stat main...feature/checkout-saved-cards | grep -iE "\\.log|node_modu'
- **Bash** command='B=feature/checkout-saved-cards; git show $B:pizza/pizza-react-frontend/src/pages/CheckoutPage.tsx | grep -n "function reloadCards\\|catch(() => setCards\\|cards.length > 0\\|listPaymentMethods"; git show'
- **Write** file_path='/Users/folaukaveinga/.claude-personal/plans/you-are-reviewing-a-curried-wave.md'
I found no blockers in PIZZA-42. There's one should-fix (the card that gets charged can differ from the one on the button) and four nits. I only read the code: I didn't run the tests, Playwright or `spotless:check`, and I changed no files. I read the PR description.

## Findings

**1. should-fix: the browser charges whatever card is on the PaymentIntent when it confirms, which may not be the card on the button.**
`SavedCardPayment.tsx:87` and `:104`. Choosing a saved card is two separate calls: the server sets the card on the order's payment, then the browser confirms. The confirm call sends no card of its own, so it uses the last card any request set.
- **Scenario A:** the customer has checkout open in two tabs. Tab 1 picks Visa ••4242 and the server sets it. Tab 2 picks Mastercard ••5555 and the server sets that. Tab 1's confirm then runs, and the "Pay with Visa ••4242" button charges ••5555.
- **Scenario B:** the order is paid in tab 1 and the webhook hasn't arrived yet, so it is still `PENDING_PAYMENT`. Tab 2's PUT passes the 409 check, and Stripe refuses to update a payment that already succeeded. `CustomerOrderServiceImpl.java:262` turns that into "That card could not be used… Please choose another card", which invites the customer to try paying again for an order that is already paid.
- **Impact:** only the customer's own cards are involved and nothing is charged twice. The confirmation page shows the card that really paid, because `captureCardDetails` reads it back from Stripe.
- **Fix:** have the PUT return the payment's status. Also turn Stripe's "already succeeded" refusal into the existing 409 rather than a 400.

**2. nit: the payment form can swap underneath the customer if the card list loads late.**
`CheckoutPage.tsx:113` and `:262`. The new-card form shows while `cards` is empty. If `listPaymentMethods` comes back after the order exists, the page swaps to `SavedCardPayment` with the primary card selected, and anything typed into the card form is lost. It's unlikely because the list loads during the details step, but nothing prevents it.

**3. nit: a failed reload hides the "card no longer available" message.**
`CheckoutPage.tsx:131`. After a 404, `reloadCards` sets `[]` if the reload fails. That unmounts `SavedCardPayment` along with its message, and a bare new-card form appears with no explanation. The PR already lists this path as untested.

**4. nit: Stripe is called inside a read-only transaction.**
`CustomerOrderServiceImpl.java:216` and `:257`. One database connection is held for the Stripe call, including up to three retries with backoff. The PR already says this; the fix is to do the lookups first and call Stripe outside the transaction.

**5. nit (CLAUDE.md): the new DAO has no `JdbcTemplate`.**
`UserPaymentMethodDAOImp.java:15`. CLAUDE.md says every DAO implementation wires in a repository and a `JdbcTemplate`, and names `ReportDAOImp` as "the one exception". The phrase "whichever of the two each method needs" arguably allows this. Either add the field or add this DAO to the documented exception.

## Areas I checked and found nothing wrong
- **Ownership and 404 vs 403:** guest orders, other customers' orders, other customers' cards and deleted cards all get 404. Ownership is part of the card query itself, and the order is filtered by user id. A deleted account also gets 404.
- **Auth rule:** the PUT rule is ordered correctly in `SecurityConfig`, and no earlier `permitAll` covers it, so `principal` can't be null in the controller.
- **Double charge:** none. A PaymentIntent can only succeed once, the amount is never sent by the client or changed, and `markPaid` and `refreshPaymentStatus` still only move an order forward from `PENDING_PAYMENT`.
- **Stripe card token:** the browser only ever sends and receives our UUID. The DTO has no card fields, and Stripe's error text is logged, not returned.
- **Expiry:** server and browser use the same rule ("valid through the expiry month") and the server is the one that refuses. The two can disagree by a few hours at a month boundary, which is harmless and documented.
- **Error handling:** `api.ts` handles 204 correctly. `customerSafeMessage` behaves exactly like the old inline code, and a decline leaves the order `PENDING_PAYMENT` so another card can be tried.
- **Retry without an idempotency key:** the PR's reasoning holds. Setting the same card again is harmless, and a key would replay stale results.

## Would the tests catch a regression?
Mostly yes, on the backend.
- The service tests check every refusal and confirm Stripe is never called when a request is refused. They assert the exact `(pi, cus, pm)` arguments, so swapped arguments or a dropped ownership filter would fail.
- The "someone else's order" case is tested only at the service level, not over HTTP. The no-token test can't tell the explicit rule from default-deny, but that's harmless because both give 403.
- In the browser, the tests that actually pay against Stripe skip when the backend has no Stripe key. Without a key, the PUT → confirm sequence and the decline-then-retry flow have no coverage; the stubbed tests only cover the UI.
- Not tested: the 404 → reload path, a failed or cancelled 3D Secure, and the two-tab case in finding 1.

## Other repo rules
- The commits have no `Co-Authored-By` trailer, as this repo's rules require.
- No logs or build output are committed.
- Every endpoint is documented in Swagger, and the services follow the interface-plus-implementation rule.
- The test count matches: 60 before plus 31 new is 91.

The review is also saved to `/Users/folaukaveinga/.claude-personal/plans/you-are-reviewing-a-curried-wave.md`.

The Stripe plugin's MCP server isn't authorized in this session, so I couldn't use it; you can connect it through `/mcp` in an interactive session.


_turns: 15, duration: 190s, cost: $1.30_

## Final answer

I found no blockers in PIZZA-42. There's one should-fix (the card that gets charged can differ from the one on the button) and four nits. I only read the code: I didn't run the tests, Playwright or `spotless:check`, and I changed no files. I read the PR description.

## Findings

**1. should-fix: the browser charges whatever card is on the PaymentIntent when it confirms, which may not be the card on the button.**
`SavedCardPayment.tsx:87` and `:104`. Choosing a saved card is two separate calls: the server sets the card on the order's payment, then the browser confirms. The confirm call sends no card of its own, so it uses the last card any request set.
- **Scenario A:** the customer has checkout open in two tabs. Tab 1 picks Visa ••4242 and the server sets it. Tab 2 picks Mastercard ••5555 and the server sets that. Tab 1's confirm then runs, and the "Pay with Visa ••4242" button charges ••5555.
- **Scenario B:** the order is paid in tab 1 and the webhook hasn't arrived yet, so it is still `PENDING_PAYMENT`. Tab 2's PUT passes the 409 check, and Stripe refuses to update a payment that already succeeded. `CustomerOrderServiceImpl.java:262` turns that into "That card could not be used… Please choose another card", which invites the customer to try paying again for an order that is already paid.
- **Impact:** only the customer's own cards are involved and nothing is charged twice. The confirmation page shows the card that really paid, because `captureCardDetails` reads it back from Stripe.
- **Fix:** have the PUT return the payment's status. Also turn Stripe's "already succeeded" refusal into the existing 409 rather than a 400.

**2. nit: the payment form can swap underneath the customer if the card list loads late.**
`CheckoutPage.tsx:113` and `:262`. The new-card form shows while `cards` is empty. If `listPaymentMethods` comes back after the order exists, the page swaps to `SavedCardPayment` with the primary card selected, and anything typed into the card form is lost. It's unlikely because the list loads during the details step, but nothing prevents it.

**3. nit: a failed reload hides the "card no longer available" message.**
`CheckoutPage.tsx:131`. After a 404, `reloadCards` sets `[]` if the reload fails. That unmounts `SavedCardPayment` along with its message, and a bare new-card form appears with no explanation. The PR already lists this path as untested.

**4. nit: Stripe is called inside a read-only transaction.**
`CustomerOrderServiceImpl.java:216` and `:257`. One database connection is held for the Stripe call, including up to three retries with backoff. The PR already says this; the fix is to do the lookups first and call Stripe outside the transaction.

**5. nit (CLAUDE.md): the new DAO has no `JdbcTemplate`.**
`UserPaymentMethodDAOImp.java:15`. CLAUDE.md says every DAO implementation wires in a repository and a `JdbcTemplate`, and names `ReportDAOImp` as "the one exception". The phrase "whichever of the two each method needs" arguably allows this. Either add the field or add this DAO to the documented exception.

## Areas I checked and found nothing wrong
- **Ownership and 404 vs 403:** guest orders, other customers' orders, other customers' cards and deleted cards all get 404. Ownership is part of the card query itself, and the order is filtered by user id. A deleted account also gets 404.
- **Auth rule:** the PUT rule is ordered correctly in `SecurityConfig`, and no earlier `permitAll` covers it, so `principal` can't be null in the controller.
- **Double charge:** none. A PaymentIntent can only succeed once, the amount is never sent by the client or changed, and `markPaid` and `refreshPaymentStatus` still only move an order forward from `PENDING_PAYMENT`.
- **Stripe card token:** the browser only ever sends and receives our UUID. The DTO has no card fields, and Stripe's error text is logged, not returned.
- **Expiry:** server and browser use the same rule ("valid through the expiry month") and the server is the one that refuses. The two can disagree by a few hours at a month boundary, which is harmless and documented.
- **Error handling:** `api.ts` handles 204 correctly. `customerSafeMessage` behaves exactly like the old inline code, and a decline leaves the order `PENDING_PAYMENT` so another card can be tried.
- **Retry without an idempotency key:** the PR's reasoning holds. Setting the same card again is harmless, and a key would replay stale results.

## Would the tests catch a regression?
Mostly yes, on the backend.
- The service tests check every refusal and confirm Stripe is never called when a request is refused. They assert the exact `(pi, cus, pm)` arguments, so swapped arguments or a dropped ownership filter would fail.
- The "someone else's order" case is tested only at the service level, not over HTTP. The no-token test can't tell the explicit rule from default-deny, but that's harmless because both give 403.
- In the browser, the tests that actually pay against Stripe skip when the backend has no Stripe key. Without a key, the PUT → confirm sequence and the decline-then-retry flow have no coverage; the stubbed tests only cover the UI.
- Not tested: the 404 → reload path, a failed or cancelled 3D Secure, and the two-tab case in finding 1.

## Other repo rules
- The commits have no `Co-Authored-By` trailer, as this repo's rules require.
- No logs or build output are committed.
- Every endpoint is documented in Swagger, and the services follow the interface-plus-implementation rule.
- The test count matches: 60 before plus 31 new is 91.

The review is also saved to `/Users/folaukaveinga/.claude-personal/plans/you-are-reviewing-a-curried-wave.md`.

The Stripe plugin's MCP server isn't authorized in this session, so I couldn't use it; you can connect it through `/mcp` in an interactive session.
