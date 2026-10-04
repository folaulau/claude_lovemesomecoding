# Session 04-analysis

mode: `plan`  cwd: `/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza`

## Prompt

```text
I've been asked to add 'pay with a saved card' to checkout in this pizza app (backend + pizza-react-frontend only for now). Before I plan anything I want to understand what's there today. Don't change any files.

1. Trace checkout end to end: from the Checkout page's pay button in pizza-react-frontend through the API to Stripe and back to an order being marked paid. Name the files and methods at each hop.
2. How are cards saved today on the profile page, and what is stored in our database vs in Stripe?
3. What existing rules or invariants in the code would a saved-card checkout have to respect?
4. Roughly how big is this change: which files would likely need to change?

Cite file paths and line numbers for every claim so I can check them.
```

## Transcript

- **Bash** command='ls; grep -rniE "stripe|paymentIntent|payment_method|paymentMethod|clientSecret" pizza-springboot-backend/src/main --include=*.java --include=*.sql --include=*.properties -l; echo ---; grep -rniE "stri'
- **Bash** command="grep -rliE 'stripe|paymentIntent|payment_method|paymentMethod|clientSecret' pizza-springboot-backend/src; echo ---; grep -rliE 'stripe|paymentMethod|clientSecret|confirmPayment|savedCard|setupIntent' "
- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend/src && cat -n pages/CheckoutPage.tsx; cat -n components/StripePaymentForm.tsx; cat -n li'
- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/main/java/com/pizza/api && cat -n payment/StripeService.java payment/StripeWebho'
- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/main/java/com/pizza/api && cat -n entity/order/CustomerOrderServiceImpl.java'
- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/main && cat -n java/com/pizza/api/entity/user/UserProfileServiceImpl.java java/c'
- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/main/java/com/pizza/api && cat -n dto/OrderCreateDTO.java dto/OrderCreateRespons'
Still tracing — backend done, now reading the profile page card flow and confirmation page.

- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-react-frontend && grep -n -i "stripe\\|setupIntent\\|confirmSetup\\|paymentMethod\\|Elements\\|addCard\\|func'
- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza && sed -n 49,90p pizza-react-frontend/src/pages/ProfilePage.tsx; sed -n 175,195p pizza-react-frontend/src/pag'
- **Bash** command='sed -n 40,60p pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/OrderApiIntegrationTest.java; grep -n -i "saved card\\|pay with a saved" progress_report.md | head; grep -n "card\\|paymen'
- **Write** file_path='/Users/folaukaveinga/.claude-personal/plans/i-ve-been-asked-to-wild-umbrella.md'
I didn't change any repo files. The only file I wrote is my own notes file outside the repo (`~/.claude-personal/plans/i-ve-been-asked-to-wild-umbrella.md`). Paths below are relative to `pizza/`.

**The main finding:** the PaymentIntent is created without a Stripe Customer (`StripeService.java:82-90`). A saved card is attached to the user's Customer, and Stripe won't charge an attached card from a PaymentIntent that has no `customer`. Wiring this up is the main backend change.

## 1. Checkout, end to end

Checkout happens in two steps. The order has to exist before the card form can render.

| # | Hop | Where |
|---|---|---|
| 1 | The "Continue to payment" button submits `#checkout-form` | `pizza-react-frontend/src/pages/CheckoutPage.tsx:494-512` |
| 2 | `handleCreateOrder` builds the order request (no prices) and POSTs `/api/orders`, sending the token only if the user is signed in | `CheckoutPage.tsx:125-170`, the POST at `:157` |
| 3 | `CustomerOrderRestController.createOrder` gets the email from `Principal`, which is null for a guest | `pizza-springboot-backend/src/main/java/com/pizza/api/entity/order/CustomerOrderRestController.java:37-44`. Guests are allowed by `config/SecurityConfig.java:117-118` |
| 4 | `CustomerOrderServiceImpl.createOrder` checks the guest email and the delivery address, prices the cart from the database (`PricingService.price`), and saves the order as `PENDING_PAYMENT` | `entity/order/CustomerOrderServiceImpl.java:47-85` |
| 5 | It then calls `StripeService.createPaymentIntent(total, publicId, email)`, stores the intent id on the order and returns the `clientSecret` | `CustomerOrderServiceImpl.java:87-108` |
| 6 | Stripe call: amount in cents, `metadata.orderId`, automatic payment methods, idempotency key `order-<uuid>`, with retries | `payment/StripeService.java:71-104` |
| 7 | When `created` is set, the page swaps to step 2 and renders `<Elements key={clientSecret}>` around `StripePaymentForm` | `CheckoutPage.tsx:205-229` |
| 8 | The "Pay $X" button calls `stripe.confirmPayment({elements, redirect:'if_required'})`. On success it only calls `onSuccess`; the browser never marks the order paid | `pizza-react-frontend/src/components/StripePaymentForm.tsx:28-68`, comment at `:62-66` |
| 9 | `handlePaymentSuccess` clears the cart and navigates to `/order-confirmation/:id` | `CheckoutPage.tsx:173-177` |
| 10a | **Polling:** `OrderConfirmationPage` polls `GET /api/orders/{id}/payment-status` up to 10 times, every 2s. `refreshPaymentStatus` fetches the intent from Stripe; if it has `succeeded`, the order becomes `PAID` and the card details are recorded | `pages/OrderConfirmationPage.tsx:17-72`, `CustomerOrderRestController.java:53-60`, `CustomerOrderServiceImpl.java:123-144` |
| 10b | **Webhook:** `StripeWebhookController.handle` checks `Stripe-Signature`, and on `payment_intent.succeeded` calls `markPaid(intentId)`. That only moves an order forward from `PENDING_PAYMENT`, so it's safe if Stripe sends the event twice | `payment/StripeWebhookController.java:46-80`, `CustomerOrderServiceImpl.java:170-195` |
| 11 | `captureCardDetails` stores only the brand and last four digits on the order. If the payment method isn't a card (Link, Cash App, Klarna), it stores the type instead | `CustomerOrderServiceImpl.java:207-238` |

## 2. How cards are saved today

**Flow:**
1. **Start setup:** the profile page's `startAddingCard` calls `POST /api/me/payment-methods/setup-intent`. `pizza-react-frontend/src/pages/ProfilePage.tsx:178-186`.
2. **Server side:** `UserProfileServiceImpl.createSetupIntent` runs `ensureCustomer`, which creates a Stripe Customer the first time and saves its id on the user. It then calls `createSetupIntent(customerId)` for a card. `entity/user/UserProfileServiceImpl.java:147-166`, `StripeService.java:132-162`.
3. **Collect the card:** `AddCardForm` calls `stripe.confirmSetup`. This saves the card without charging it. `ProfilePage.tsx:41-90`.
4. **Save it:** only the resulting `pm_…` id is POSTed to `/api/me/payment-methods`. `ProfilePage.tsx:68-77`, `lib/profileApi.ts:29-30`.
5. **Server side:** `addPaymentMethod` attaches the card to the Customer, reads back brand, last4 and expiry, and saves a row. The first card saved automatically becomes primary, and any other primary is demoted. `UserProfileServiceImpl.java:168-211`, `:294-301`.

**What's stored where:**
- **Stripe** holds the card itself and the Customer it's attached to.
- **Our database:**
  - `app_user.stripe_customer_id` (`008-user-addresses-and-payment-methods.sql:20-24`, `User.java:77-78`).
  - `user_payment_method` holds the `pm_` token, brand, last4, expiry month and year, `is_primary` and `deleted`. There is a unique constraint on (user, token). `008-…sql:52-69`, `UserPaymentMethod.java:66-89`.
  - `customer_order` stores only `card_brand` and `card_last4`, never the token (`009-order-card-details.sql:6-13`).
- **The browser** sees our UUID plus display fields, never the token (`dto/PaymentMethodDTO.java:9-19`, `types/index.ts:315-325`).
- **Deleting a card** detaches it at Stripe and soft-deletes the row (`UserProfileServiceImpl.java:225-253`).

## 3. Rules a saved-card checkout has to respect

1. **The intent needs `customer` set.** It currently has none (`StripeService.java:82-90`). Use `user.getStripeCustomerId()`; any user with saved cards already has one.
2. **The idempotency key is `order-<uuid>`** (`StripeService.java:100-101`). Stripe returns an error if the same key is reused with different parameters. So either choose the card when the order is created (step 1), or attach it later with a PaymentIntent *update*, not a second *create*.
3. **The browser sends our UUID, not `pm_`** (`PaymentMethodDTO.java:9-10`). The server converts the UUID to the token after an ownership check. A card belonging to someone else must return **404, not 403**. The existing check is private: `requireOwnedPaymentMethod`, `UserProfileServiceImpl.java:264-282`.
4. **Guest checkout must still work** (`CustomerOrderRestController.java:31-44`, `SecurityConfig.java:116-118`). A saved card only makes sense when signed in, so a guest who sends a card id should be rejected.
5. **Server-side pricing is unchanged.** No amounts come from the client (`OrderCreateDTO.java:16-25`, `CustomerOrderServiceImpl.java:59-60`).
6. **The browser never marks an order paid.** `PAID` comes only from `markPaid` or `refreshPaymentStatus` (`StripePaymentForm.tsx:62-66`). If you keep confirmation in the browser, Stripe.js also handles 3D Secure for a saved card.
7. **No card data, and no token on the order** (`UserPaymentMethod.java:24-34`, `009-…sql:6-8`, `CustomerOrderServiceImpl.java:197-202`). `captureCardDetails` already works for saved cards.
8. **Deleted cards are hidden automatically** by `@SQLRestriction` (`UserPaymentMethod.java:42`). Expiry is stored, so expired cards can be filtered or disabled.
9. **"Stripe not configured" path:** `clientSecret` stays null and the page shows a warning (`CustomerOrderServiceImpl.java:87-101`, `CheckoutPage.tsx:230-237`). Profile already has the same kind of check (`UserProfileServiceImpl.java:303-308`).
10. **DAO rule from `CLAUDE.md`:** `UserProfileServiceImpl` calls repositories directly (`:26-30`). Adding a card lookup to the order service is a chance to put it behind a DAO rather than copy that.
11. **Reuse the address chooser pattern:** the checkout already has a radio list with the primary preselected and a "use a different one" option (`CheckoutPage.tsx:40-49`, `:70-96`, `:339-372`).

## 4. Rough size: small to medium, no schema change

**Backend (about 4–5 files):**
- `dto/OrderCreateDTO.java`: add an optional `UUID paymentMethodId`.
- `CustomerOrderServiceImpl.createOrder`: reject guests who send one, resolve an owned card, and pass the customer and card to Stripe.
- `StripeService.createPaymentIntent`: accept a customer id and a card id.
- A shared ownership lookup, either a new `UserPaymentMethodDAO`/`DAOImp` or one pulled out of `UserProfileServiceImpl`.
- Tests: `OrderApiIntegrationTest` already mocks `StripeService` (`:43-49`). Add cases for a guest sending a card (400), someone else's card (404), and your own card (customer and card reach Stripe).

**Frontend (about 3–4 files):**
- `types/index.ts`: add `paymentMethodId?` to `OrderCreateRequest` (`:146`).
- `CheckoutPage.tsx`: load `profileApi.listPaymentMethods()`, add a card chooser, and branch step 2.
- A small saved-card pay component that confirms with the `clientSecret` and no Elements, alongside `StripePaymentForm`.
- Playwright: extend `e2e/checkout.spec.ts` or `e2e/profile.spec.ts`; the automatable Stripe confirmation goes in `e2e/payment.spec.ts`, following its existing pattern.

**Unchanged:** the webhook, `markPaid`, `refreshPaymentStatus`, `captureCardDetails`, the confirmation page, the Liquibase changesets and the security config. After this the "checkout doesn't offer saved cards" note in `CLAUDE.md` and `progress_report.md:1063, 1504` will be out of date for React only; the other three frontends still won't offer them.

Before building, decide whether the customer picks the card in step 1 (simplest, and avoids the idempotency-key conflict) or after the order exists (needs a PaymentIntent update endpoint).


_turns: 12, duration: 101s, cost: $1.05_

## Final answer

I didn't change any repo files. The only file I wrote is my own notes file outside the repo (`~/.claude-personal/plans/i-ve-been-asked-to-wild-umbrella.md`). Paths below are relative to `pizza/`.

**The main finding:** the PaymentIntent is created without a Stripe Customer (`StripeService.java:82-90`). A saved card is attached to the user's Customer, and Stripe won't charge an attached card from a PaymentIntent that has no `customer`. Wiring this up is the main backend change.

## 1. Checkout, end to end

Checkout happens in two steps. The order has to exist before the card form can render.

| # | Hop | Where |
|---|---|---|
| 1 | The "Continue to payment" button submits `#checkout-form` | `pizza-react-frontend/src/pages/CheckoutPage.tsx:494-512` |
| 2 | `handleCreateOrder` builds the order request (no prices) and POSTs `/api/orders`, sending the token only if the user is signed in | `CheckoutPage.tsx:125-170`, the POST at `:157` |
| 3 | `CustomerOrderRestController.createOrder` gets the email from `Principal`, which is null for a guest | `pizza-springboot-backend/src/main/java/com/pizza/api/entity/order/CustomerOrderRestController.java:37-44`. Guests are allowed by `config/SecurityConfig.java:117-118` |
| 4 | `CustomerOrderServiceImpl.createOrder` checks the guest email and the delivery address, prices the cart from the database (`PricingService.price`), and saves the order as `PENDING_PAYMENT` | `entity/order/CustomerOrderServiceImpl.java:47-85` |
| 5 | It then calls `StripeService.createPaymentIntent(total, publicId, email)`, stores the intent id on the order and returns the `clientSecret` | `CustomerOrderServiceImpl.java:87-108` |
| 6 | Stripe call: amount in cents, `metadata.orderId`, automatic payment methods, idempotency key `order-<uuid>`, with retries | `payment/StripeService.java:71-104` |
| 7 | When `created` is set, the page swaps to step 2 and renders `<Elements key={clientSecret}>` around `StripePaymentForm` | `CheckoutPage.tsx:205-229` |
| 8 | The "Pay $X" button calls `stripe.confirmPayment({elements, redirect:'if_required'})`. On success it only calls `onSuccess`; the browser never marks the order paid | `pizza-react-frontend/src/components/StripePaymentForm.tsx:28-68`, comment at `:62-66` |
| 9 | `handlePaymentSuccess` clears the cart and navigates to `/order-confirmation/:id` | `CheckoutPage.tsx:173-177` |
| 10a | **Polling:** `OrderConfirmationPage` polls `GET /api/orders/{id}/payment-status` up to 10 times, every 2s. `refreshPaymentStatus` fetches the intent from Stripe; if it has `succeeded`, the order becomes `PAID` and the card details are recorded | `pages/OrderConfirmationPage.tsx:17-72`, `CustomerOrderRestController.java:53-60`, `CustomerOrderServiceImpl.java:123-144` |
| 10b | **Webhook:** `StripeWebhookController.handle` checks `Stripe-Signature`, and on `payment_intent.succeeded` calls `markPaid(intentId)`. That only moves an order forward from `PENDING_PAYMENT`, so it's safe if Stripe sends the event twice | `payment/StripeWebhookController.java:46-80`, `CustomerOrderServiceImpl.java:170-195` |
| 11 | `captureCardDetails` stores only the brand and last four digits on the order. If the payment method isn't a card (Link, Cash App, Klarna), it stores the type instead | `CustomerOrderServiceImpl.java:207-238` |

## 2. How cards are saved today

**Flow:**
1. **Start setup:** the profile page's `startAddingCard` calls `POST /api/me/payment-methods/setup-intent`. `pizza-react-frontend/src/pages/ProfilePage.tsx:178-186`.
2. **Server side:** `UserProfileServiceImpl.createSetupIntent` runs `ensureCustomer`, which creates a Stripe Customer the first time and saves its id on the user. It then calls `createSetupIntent(customerId)` for a card. `entity/user/UserProfileServiceImpl.java:147-166`, `StripeService.java:132-162`.
3. **Collect the card:** `AddCardForm` calls `stripe.confirmSetup`. This saves the card without charging it. `ProfilePage.tsx:41-90`.
4. **Save it:** only the resulting `pm_…` id is POSTed to `/api/me/payment-methods`. `ProfilePage.tsx:68-77`, `lib/profileApi.ts:29-30`.
5. **Server side:** `addPaymentMethod` attaches the card to the Customer, reads back brand, last4 and expiry, and saves a row. The first card saved automatically becomes primary, and any other primary is demoted. `UserProfileServiceImpl.java:168-211`, `:294-301`.

**What's stored where:**
- **Stripe** holds the card itself and the Customer it's attached to.
- **Our database:**
  - `app_user.stripe_customer_id` (`008-user-addresses-and-payment-methods.sql:20-24`, `User.java:77-78`).
  - `user_payment_method` holds the `pm_` token, brand, last4, expiry month and year, `is_primary` and `deleted`. There is a unique constraint on (user, token). `008-…sql:52-69`, `UserPaymentMethod.java:66-89`.
  - `customer_order` stores only `card_brand` and `card_last4`, never the token (`009-order-card-details.sql:6-13`).
- **The browser** sees our UUID plus display fields, never the token (`dto/PaymentMethodDTO.java:9-19`, `types/index.ts:315-325`).
- **Deleting a card** detaches it at Stripe and soft-deletes the row (`UserProfileServiceImpl.java:225-253`).

## 3. Rules a saved-card checkout has to respect

1. **The intent needs `customer` set.** It currently has none (`StripeService.java:82-90`). Use `user.getStripeCustomerId()`; any user with saved cards already has one.
2. **The idempotency key is `order-<uuid>`** (`StripeService.java:100-101`). Stripe returns an error if the same key is reused with different parameters. So either choose the card when the order is created (step 1), or attach it later with a PaymentIntent *update*, not a second *create*.
3. **The browser sends our UUID, not `pm_`** (`PaymentMethodDTO.java:9-10`). The server converts the UUID to the token after an ownership check. A card belonging to someone else must return **404, not 403**. The existing check is private: `requireOwnedPaymentMethod`, `UserProfileServiceImpl.java:264-282`.
4. **Guest checkout must still work** (`CustomerOrderRestController.java:31-44`, `SecurityConfig.java:116-118`). A saved card only makes sense when signed in, so a guest who sends a card id should be rejected.
5. **Server-side pricing is unchanged.** No amounts come from the client (`OrderCreateDTO.java:16-25`, `CustomerOrderServiceImpl.java:59-60`).
6. **The browser never marks an order paid.** `PAID` comes only from `markPaid` or `refreshPaymentStatus` (`StripePaymentForm.tsx:62-66`). If you keep confirmation in the browser, Stripe.js also handles 3D Secure for a saved card.
7. **No card data, and no token on the order** (`UserPaymentMethod.java:24-34`, `009-…sql:6-8`, `CustomerOrderServiceImpl.java:197-202`). `captureCardDetails` already works for saved cards.
8. **Deleted cards are hidden automatically** by `@SQLRestriction` (`UserPaymentMethod.java:42`). Expiry is stored, so expired cards can be filtered or disabled.
9. **"Stripe not configured" path:** `clientSecret` stays null and the page shows a warning (`CustomerOrderServiceImpl.java:87-101`, `CheckoutPage.tsx:230-237`). Profile already has the same kind of check (`UserProfileServiceImpl.java:303-308`).
10. **DAO rule from `CLAUDE.md`:** `UserProfileServiceImpl` calls repositories directly (`:26-30`). Adding a card lookup to the order service is a chance to put it behind a DAO rather than copy that.
11. **Reuse the address chooser pattern:** the checkout already has a radio list with the primary preselected and a "use a different one" option (`CheckoutPage.tsx:40-49`, `:70-96`, `:339-372`).

## 4. Rough size: small to medium, no schema change

**Backend (about 4–5 files):**
- `dto/OrderCreateDTO.java`: add an optional `UUID paymentMethodId`.
- `CustomerOrderServiceImpl.createOrder`: reject guests who send one, resolve an owned card, and pass the customer and card to Stripe.
- `StripeService.createPaymentIntent`: accept a customer id and a card id.
- A shared ownership lookup, either a new `UserPaymentMethodDAO`/`DAOImp` or one pulled out of `UserProfileServiceImpl`.
- Tests: `OrderApiIntegrationTest` already mocks `StripeService` (`:43-49`). Add cases for a guest sending a card (400), someone else's card (404), and your own card (customer and card reach Stripe).

**Frontend (about 3–4 files):**
- `types/index.ts`: add `paymentMethodId?` to `OrderCreateRequest` (`:146`).
- `CheckoutPage.tsx`: load `profileApi.listPaymentMethods()`, add a card chooser, and branch step 2.
- A small saved-card pay component that confirms with the `clientSecret` and no Elements, alongside `StripePaymentForm`.
- Playwright: extend `e2e/checkout.spec.ts` or `e2e/profile.spec.ts`; the automatable Stripe confirmation goes in `e2e/payment.spec.ts`, following its existing pattern.

**Unchanged:** the webhook, `markPaid`, `refreshPaymentStatus`, `captureCardDetails`, the confirmation page, the Liquibase changesets and the security config. After this the "checkout doesn't offer saved cards" note in `CLAUDE.md` and `progress_report.md:1063, 1504` will be out of date for React only; the other three frontends still won't offer them.

Before building, decide whether the customer picks the card in step 1 (simplest, and avoids the idempotency-key conflict) or after the order exists (needs a PaymentIntent update endpoint).
