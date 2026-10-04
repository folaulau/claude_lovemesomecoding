# Session 06-planning

mode: `plan`  cwd: `/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza`  resumed: `aa622bee-305d-4a91-bbfa-0b046bb02d30`

## Prompt

```text
The product owner answered:
- Q1: out of scope. Saving a card at checkout becomes a separate ticket.
- Q3/Q5: choose the card on the payment step. On a decline, show it and let them pick another saved card or enter a new one on the same order.
- Q4: expired cards are shown but disabled, labelled Expired.
- Q8: backend + pizza-react-frontend only.
- Q2, Q6, Q7, Q9: your defaults are accepted (primary preselected, no CVC re-entry, explicit 'Pay $X with Visa ••4242' button, no card management at checkout).

Write the implementation plan. Requirements for the plan:
- Split into numbered steps, each small enough to be ONE reviewable commit, backend before frontend.
- For each step: the files it touches, what changes, and how we verify it before moving on (which test, which command).
- Follow the rules in CLAUDE.md (DAO rule, service interface + impl, 404 not 403, spotless, never edit an applied changeset).
- List explicitly what is OUT of scope, so I can hold every later diff against this plan.
Don't write any code yet.
```

## Transcript

- **Bash** command='B=pizza-springboot-backend/src; find $B/test -type f | sed \'s|.*/test/||\'; grep -n "static ApiException" $B/main/java/com/pizza/api/exception/ApiException.java; cat -n $B/main/java/com/pizza/api/entit'
- **Bash** command='B=pizza-springboot-backend/src; sed -n 1,75p $B/main/java/com/pizza/api/exception/ApiException.java; cat -n $B/main/java/com/pizza/api/entity/user/UserDAO.java; sed -n 1,60p $B/main/java/com/pizza/api'
- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend && sed -n 29,110p e2e/payment.spec.ts; grep -n "\\"test\\|\\"lint\\|\\"build\\|typecheck" pack'
- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza && sed -n 1,40p pizza-springboot-backend/src/test/java/com/pizza/api/entity/product/ProductServiceImplTest.ja'
- **Write** file_path='/Users/folaukaveinga/.claude-personal/plans/i-ve-been-asked-to-wild-umbrella.md'
# PIZZA-42: pay with a saved card at checkout — implementation plan

Order creation stays exactly as it is. One new authenticated endpoint, `PUT /api/orders/{id}/payment-method`, takes our card UUID. After checking ownership, the server puts the user's Stripe customer and the saved card onto the order's **existing** PaymentIntent. The browser then calls `stripe.confirmCardPayment(clientSecret)`, which uses the card the server set and runs 3D Secure if the bank asks for it.

How orders get marked PAID doesn't change (webhook, plus the confirmation page polling). After a decline, Stripe lets a different card be set on the same PaymentIntent, so a second saved card or a new card can pay for the same order. The `pm_` token never reaches the browser.

**Two decisions to check in review:**
- **The update call has no idempotency key, on purpose.** A key per order and card would make a later switch from card A to B and back to A return Stripe's saved result from the first A request without changing anything. Setting the same values twice is already safe.
- **The card is chosen on the payment step,** as the PO asked. That's why this updates the PaymentIntent rather than adding a field to the order request.

## Steps (one commit each)

**1. Backend: data access and expiry rule**
- New `entity/user/UserPaymentMethodDAO` and `UserPaymentMethodDAOImp`. They use the repository plus a JdbcTemplate, with `UserDAOImp` as the model. The one method is `findOwned(userId, publicId)`.
- `UserPaymentMethodRepository`: add `findByPublicIdAndUserId`.
- `UserPaymentMethod`: add `isExpiredAt(YearMonth)`. A card is valid through the end of its expiry month; no expiry means not expired.
- **Verify:**
  - New `UserPaymentMethodDAOIntegrationTest`: your own card is found; another user's card and a deleted card are not.
  - New `UserPaymentMethodTest`: month boundaries, and no expiry.
  - Run `./mvnw spotless:apply && ./mvnw test`.

**2. Backend: service method and Stripe update**
- `ApiException`: add `conflict()`, which returns 409.
- `StripeService`: add `attachSavedCardToPaymentIntent(intentId, customerId, pmId)`, using `@Retryable` and no idempotency key, with a comment explaining why.
- `CustomerOrderService` and `CustomerOrderServiceImpl`: add `useSavedPaymentMethod(orderId, paymentMethodId, email)`. Checks, in order:
  1. Order missing, a guest order, or someone else's → 404.
  2. Order not waiting for payment → 409.
  3. Stripe not set up, or no PaymentIntent on the order → 400.
  4. Card not yours, or deleted → 404 (not 403).
  5. Card expired → 400.
  6. Stripe rejects the update → 400, and the order is left unchanged.
- **Verify:** new `CustomerOrderSavedCardTest` (a Spring Boot test with Stripe mocked) covering every check, and that the success case sends the payment, customer and card ids to Stripe. Then spotless and `./mvnw test`.

**3. Backend: endpoint and security rule**
- New `dto/SavedPaymentMethodDTO(@NotNull UUID paymentMethodId)`.
- New `PUT /api/orders/{id}/payment-method` on `CustomerOrderRestController`, documented in Swagger, returning 204.
- `SecurityConfig`: name the new route explicitly as authenticated. The catch-all rule would already block it, but every other route is listed by name.
- **Verify:** new `SavedCardPaymentApiIntegrationTest`, using real login tokens:
  - No token → 401.
  - Paying a guest's order → 404.
  - Using the admin's card → 404.
  - Your own deleted card → 404.
  - Expired card → 400.
  - Missing body → 400.
  - Order already paid → 409.
  - Valid request → 204.

  Then `./mvnw test`, and check the endpoint appears in Swagger.

**4. Frontend: helpers, no visible change**
- New `lib/cards.ts`: `isCardExpired` and `cardLabel` ("Visa ••4242", safe when brand or last4 is missing).
- New `lib/stripeErrors.ts`: moves the "which Stripe errors are safe to show" logic out of `StripePaymentForm.tsx:50-57` without changing behaviour.
- New `lib/orderApi.ts`: `useSavedCard(orderId, paymentMethodId)`.
- **Verify:** `npm run typecheck && npm run lint && npm run build`, then `npx playwright test e2e/checkout.spec.ts` to confirm nothing changed.

**5. Frontend: card chooser on the payment step**
- New `components/SavedCardPayment.tsx`, inside the existing Stripe `<Elements>` wrapper:
  - A radio list of cards. Expired cards are disabled with an "Expired" badge.
  - A "Use a new card" option that shows the unchanged `StripePaymentForm`.
  - Starts on the primary card if it's valid, otherwise the first valid card, otherwise a new card.
  - A "Pay $X with Visa ••4242" button that sends the PUT, then calls `confirmCardPayment`.
  - On an error, it shows the message and keeps the chooser usable on the same order.
  - If the card was deleted meanwhile (404), it says the card is no longer available and reloads the list.
- `CheckoutPage.tsx`: signed-in users load their cards alongside their addresses. If that fails, they get the new-card form. Guests see no change.
- **Verify:** typecheck, lint and build. Then by hand, with both apps running:
  - The primary card is preselected and the button reads correctly.
  - A successful payment shows PAID and "Visa ending 4242" on the confirmation page.
  - The 3D Secure test card `4000 0025 0000 3155` brings up the challenge.
  - After a decline, a new card pays for the same order.

**6. Frontend: Playwright**
- New `e2e/saved-card-checkout.spec.ts`, added to the `test:e2e` list in `package.json`.
- **With a stubbed card list** (no Stripe needed): an expired card is disabled and labelled, the primary is preselected, the button label is right, and guests see no chooser.
- **Live** (skipped when the backend has no Stripe key):
  - Save `pm_card_visa` through our own API, pay with it in the UI, and check the order is PAID.
  - Save a card that is declined when charged plus a good one: the first payment is declined, the second succeeds, and the order id stays the same.
  - Check the result with SQL against `customer_order`.
  - Remove the saved cards afterwards.
- A new card after a decline, and 3D Secure, stay manual checks: Stripe's card iframe can't be driven by an automated browser.
- **Verify:** `npm run test:all`, with no other test suite running against the backend.

**7. Docs**
- `pizza/CLAUDE.md`: update the "Still open" note (React done; Angular and both mobile apps not) and the backend test count.
- `progress_report.md`: record the decisions, test results and manual QA.

## Out of scope — reject in review if it appears
- Saving a card at checkout (separate ticket).
- Angular, React Native and iOS.
- Re-entering the CVC.
- Adding, deleting or changing the primary card from checkout.
- Any change to order creation, the order request, how the PaymentIntent is created, the webhook, the code that marks orders paid or records the card used, or the confirmation page.
- Any database migration, and any edit to changesets 001–009.
- Moving the profile service onto the new DAO (a follow-up).
- Charging the card from the server without the customer present, refunds, wallets and admin screens.
- Existing problems: refreshing the payment step loses the order, and abandoned unpaid orders pile up.
- Rolling the Stripe secret key.

## Risks to check first, in the step 5 manual run
- I haven't confirmed that `confirmCardPayment` works with how the PaymentIntent is created today. If it doesn't, the fallback is `stripe.confirmPayment({clientSecret})`.
- I haven't confirmed whether an automated browser can confirm a saved-card payment. If it can't, the live tests confirm through Stripe's API, the way `payment.spec.ts` already does.

The plan is also saved at `~/.claude-personal/plans/i-ve-been-asked-to-wild-umbrella.md`.

**Decision for you:** your instruction files disagree on commit attribution. Your global `CLAUDE.md` requires a `Co-Authored-By: Claude` line on every commit; the project's `CLAUDE.md` says never add one. Which should these seven commits follow? Either way I won't push.


_turns: 6, duration: 166s, cost: $1.95_

## Final answer

# PIZZA-42: pay with a saved card at checkout — implementation plan

Order creation stays exactly as it is. One new authenticated endpoint, `PUT /api/orders/{id}/payment-method`, takes our card UUID. After checking ownership, the server puts the user's Stripe customer and the saved card onto the order's **existing** PaymentIntent. The browser then calls `stripe.confirmCardPayment(clientSecret)`, which uses the card the server set and runs 3D Secure if the bank asks for it.

How orders get marked PAID doesn't change (webhook, plus the confirmation page polling). After a decline, Stripe lets a different card be set on the same PaymentIntent, so a second saved card or a new card can pay for the same order. The `pm_` token never reaches the browser.

**Two decisions to check in review:**
- **The update call has no idempotency key, on purpose.** A key per order and card would make a later switch from card A to B and back to A return Stripe's saved result from the first A request without changing anything. Setting the same values twice is already safe.
- **The card is chosen on the payment step,** as the PO asked. That's why this updates the PaymentIntent rather than adding a field to the order request.

## Steps (one commit each)

**1. Backend: data access and expiry rule**
- New `entity/user/UserPaymentMethodDAO` and `UserPaymentMethodDAOImp`. They use the repository plus a JdbcTemplate, with `UserDAOImp` as the model. The one method is `findOwned(userId, publicId)`.
- `UserPaymentMethodRepository`: add `findByPublicIdAndUserId`.
- `UserPaymentMethod`: add `isExpiredAt(YearMonth)`. A card is valid through the end of its expiry month; no expiry means not expired.
- **Verify:**
  - New `UserPaymentMethodDAOIntegrationTest`: your own card is found; another user's card and a deleted card are not.
  - New `UserPaymentMethodTest`: month boundaries, and no expiry.
  - Run `./mvnw spotless:apply && ./mvnw test`.

**2. Backend: service method and Stripe update**
- `ApiException`: add `conflict()`, which returns 409.
- `StripeService`: add `attachSavedCardToPaymentIntent(intentId, customerId, pmId)`, using `@Retryable` and no idempotency key, with a comment explaining why.
- `CustomerOrderService` and `CustomerOrderServiceImpl`: add `useSavedPaymentMethod(orderId, paymentMethodId, email)`. Checks, in order:
  1. Order missing, a guest order, or someone else's → 404.
  2. Order not waiting for payment → 409.
  3. Stripe not set up, or no PaymentIntent on the order → 400.
  4. Card not yours, or deleted → 404 (not 403).
  5. Card expired → 400.
  6. Stripe rejects the update → 400, and the order is left unchanged.
- **Verify:** new `CustomerOrderSavedCardTest` (a Spring Boot test with Stripe mocked) covering every check, and that the success case sends the payment, customer and card ids to Stripe. Then spotless and `./mvnw test`.

**3. Backend: endpoint and security rule**
- New `dto/SavedPaymentMethodDTO(@NotNull UUID paymentMethodId)`.
- New `PUT /api/orders/{id}/payment-method` on `CustomerOrderRestController`, documented in Swagger, returning 204.
- `SecurityConfig`: name the new route explicitly as authenticated. The catch-all rule would already block it, but every other route is listed by name.
- **Verify:** new `SavedCardPaymentApiIntegrationTest`, using real login tokens:
  - No token → 401.
  - Paying a guest's order → 404.
  - Using the admin's card → 404.
  - Your own deleted card → 404.
  - Expired card → 400.
  - Missing body → 400.
  - Order already paid → 409.
  - Valid request → 204.

  Then `./mvnw test`, and check the endpoint appears in Swagger.

**4. Frontend: helpers, no visible change**
- New `lib/cards.ts`: `isCardExpired` and `cardLabel` ("Visa ••4242", safe when brand or last4 is missing).
- New `lib/stripeErrors.ts`: moves the "which Stripe errors are safe to show" logic out of `StripePaymentForm.tsx:50-57` without changing behaviour.
- New `lib/orderApi.ts`: `useSavedCard(orderId, paymentMethodId)`.
- **Verify:** `npm run typecheck && npm run lint && npm run build`, then `npx playwright test e2e/checkout.spec.ts` to confirm nothing changed.

**5. Frontend: card chooser on the payment step**
- New `components/SavedCardPayment.tsx`, inside the existing Stripe `<Elements>` wrapper:
  - A radio list of cards. Expired cards are disabled with an "Expired" badge.
  - A "Use a new card" option that shows the unchanged `StripePaymentForm`.
  - Starts on the primary card if it's valid, otherwise the first valid card, otherwise a new card.
  - A "Pay $X with Visa ••4242" button that sends the PUT, then calls `confirmCardPayment`.
  - On an error, it shows the message and keeps the chooser usable on the same order.
  - If the card was deleted meanwhile (404), it says the card is no longer available and reloads the list.
- `CheckoutPage.tsx`: signed-in users load their cards alongside their addresses. If that fails, they get the new-card form. Guests see no change.
- **Verify:** typecheck, lint and build. Then by hand, with both apps running:
  - The primary card is preselected and the button reads correctly.
  - A successful payment shows PAID and "Visa ending 4242" on the confirmation page.
  - The 3D Secure test card `4000 0025 0000 3155` brings up the challenge.
  - After a decline, a new card pays for the same order.

**6. Frontend: Playwright**
- New `e2e/saved-card-checkout.spec.ts`, added to the `test:e2e` list in `package.json`.
- **With a stubbed card list** (no Stripe needed): an expired card is disabled and labelled, the primary is preselected, the button label is right, and guests see no chooser.
- **Live** (skipped when the backend has no Stripe key):
  - Save `pm_card_visa` through our own API, pay with it in the UI, and check the order is PAID.
  - Save a card that is declined when charged plus a good one: the first payment is declined, the second succeeds, and the order id stays the same.
  - Check the result with SQL against `customer_order`.
  - Remove the saved cards afterwards.
- A new card after a decline, and 3D Secure, stay manual checks: Stripe's card iframe can't be driven by an automated browser.
- **Verify:** `npm run test:all`, with no other test suite running against the backend.

**7. Docs**
- `pizza/CLAUDE.md`: update the "Still open" note (React done; Angular and both mobile apps not) and the backend test count.
- `progress_report.md`: record the decisions, test results and manual QA.

## Out of scope — reject in review if it appears
- Saving a card at checkout (separate ticket).
- Angular, React Native and iOS.
- Re-entering the CVC.
- Adding, deleting or changing the primary card from checkout.
- Any change to order creation, the order request, how the PaymentIntent is created, the webhook, the code that marks orders paid or records the card used, or the confirmation page.
- Any database migration, and any edit to changesets 001–009.
- Moving the profile service onto the new DAO (a follow-up).
- Charging the card from the server without the customer present, refunds, wallets and admin screens.
- Existing problems: refreshing the payment step loses the order, and abandoned unpaid orders pile up.
- Rolling the Stripe secret key.

## Risks to check first, in the step 5 manual run
- I haven't confirmed that `confirmCardPayment` works with how the PaymentIntent is created today. If it doesn't, the fallback is `stripe.confirmPayment({clientSecret})`.
- I haven't confirmed whether an automated browser can confirm a saved-card payment. If it can't, the live tests confirm through Stripe's API, the way `payment.spec.ts` already does.

The plan is also saved at `~/.claude-personal/plans/i-ve-been-asked-to-wild-umbrella.md`.

**Decision for you:** your instruction files disagree on commit attribution. Your global `CLAUDE.md` requires a `Co-Authored-By: Claude` line on every commit; the project's `CLAUDE.md` says never add one. Which should these seven commits follow? Either way I won't push.
