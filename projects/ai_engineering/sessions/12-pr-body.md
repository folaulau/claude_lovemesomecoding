# PIZZA-42: Pay with a saved card at checkout (backend + React)

## What and why

Signed-in customers could already save cards on their profile page, but checkout always asked for a
new card. Now the checkout's payment step lists their saved cards and lets them pay with one. The
primary card is selected by default. Expired cards are listed but can't be selected, and "Use a new
card" falls back to the existing card form. If a saved card is declined, the customer can try another
saved card or a new one **on the same order**.

Scope is the Spring Boot backend and `pizza-react-frontend`. Guest checkout, the Angular app and the
two mobile apps are unchanged. There are no schema changes.

## How it works

1. The order is created exactly as before. `POST /api/orders` is unchanged and still opens a
   PaymentIntent.
2. On the payment step, the browser loads `GET /api/me/payment-methods` (signed-in users only).
3. **New: `PUT /api/orders/{id}/payment-method`** with `{ "paymentMethodId": "<our card UUID>" }`.
   `CustomerOrderServiceImpl.useSavedPaymentMethod` checks, in order:
   - the order exists and belongs to the caller. A guest order, someone else's order and an unknown
     order all return **404**;
   - it is still `PENDING_PAYMENT` → otherwise **409**;
   - Stripe is configured and the order has a PaymentIntent → otherwise **400**;
   - the card is the caller's and not deleted → otherwise **404**;
   - the card has not expired → otherwise **400**.

   It then **updates the order's existing PaymentIntent** with the user's Stripe `customer` and the
   card's `payment_method` (`StripeService.attachSavedCardToPaymentIntent`). It returns 204, and
   nothing is charged at this point.
4. The browser calls `stripe.confirmCardPayment(clientSecret)` with the client secret it already
   holds. Stripe uses the card the server set, and shows the 3D Secure challenge if the bank asks
   for one.
5. The order becomes PAID the way it always has, through the webhook or the confirmation page's
   `payment-status` poll. The browser never marks anything paid.

The Stripe `pm_…` token never reaches the browser. The request carries our UUID, and the server looks
the token up after the ownership check.

## Decisions worth checking

- **Update the existing PaymentIntent rather than create a new one.** The card is chosen after the
  order exists, and the page already holds that intent's client secret. After a decline Stripe sets
  the intent back to `requires_payment_method`, so the same endpoint can set a different card. A new
  card typed into the existing form confirms the same intent too.
- **No idempotency key on the update** (`createPaymentIntent` keeps its `order-<id>` key). For a
  repeated key, Stripe returns the stored response and does nothing. A key per (order, card) would
  make "card A, then B, then A" replay the first answer and leave B on the intent. Retrying an update
  that sets the same two fields is already harmless.
- **404, never 403**, for any order or card that isn't the caller's, so the endpoint can't confirm
  an id exists. That includes a token whose account no longer exists.
- **A request without a token gets 403, not 401.** That is how every protected endpoint in this app
  behaves (no `AuthenticationEntryPoint` is configured; `ApiSecurityIntegrationTest` already asserts
  403). The new security rule follows it rather than changing it.
- **When Stripe refuses the update, the API returns a generic message** and logs Stripe's own text —
  except when the intent has already succeeded at Stripe (paid in another tab, webhook not yet in):
  the service re-checks the intent's status and answers 409 "already been paid", so the customer is
  never invited to pay twice.
  `createOrder` still returns Stripe's message ("Could not start payment: …"), so the two paths
  differ. Aligning them is listed as a follow-up.
- **Expiry rule:** a card is valid through its expiry month, and a card with no expiry recorded is
  not treated as expired. The server (`UserPaymentMethod.isExpiredAt(YearMonth.now())`) is what
  refuses an expired card; the browser's `isCardExpired` only greys it out.
- `useSavedPaymentMethod` is `@Transactional(readOnly = true)` and calls Stripe inside it, so one
  database connection is held for the length of the Stripe call.
- Two extra guards: a missing user email returns 401, and a user with no `stripe_customer_id`
  returns 400. Neither is reachable in normal use.
- `UserPaymentMethodDAOImp` uses the repository only, with no `JdbcTemplate` yet: every query it has
  is a single-row lookup. Its class comment says so.

## Files

**Backend**
- `UserPaymentMethodDAO` / `UserPaymentMethodDAOImp`: a new DAO with `findOwned(userId, publicId)`.
- `UserPaymentMethodRepository`: new `findByPublicIdAndUserId`.
- `UserPaymentMethod`: new `isExpiredAt(YearMonth)`.
- `CustomerOrderService` / `CustomerOrderServiceImpl`: new `useSavedPaymentMethod`.
- `StripeService`: new `attachSavedCardToPaymentIntent`.
- `ApiException`: new `conflict()` (409).
- New `SavedPaymentMethodDTO`.
- `CustomerOrderRestController`: new `PUT /api/orders/{id}/payment-method`, documented for Swagger.
- `SecurityConfig`: an explicit rule making that PUT require sign-in.

**Frontend (`pizza-react-frontend`)**
- New `components/SavedCardPayment.tsx`: the card chooser (a `fieldset` with a "Pay with"
  `legend`) and the saved-card Pay button.
- `pages/CheckoutPage.tsx`: loads saved cards for signed-in users and shows the chooser on the
  payment step when there are any. If the list fails to load, the existing card form is shown.
- New `lib/cards.ts` (`isCardExpired`, `cardLabel`), `lib/orderApi.ts` (`selectSavedCard`) and
  `lib/stripeErrors.ts` (`customerSafeMessage`).
- `components/StripePaymentForm.tsx`: its "which Stripe errors are safe to show" rule moved into
  `lib/stripeErrors.ts`; behaviour unchanged.

**Docs:** `CLAUDE.md` and `progress_report.md`.

## Testing

**Backend: `./mvnw test`: 94 tests; 90–91 pass, depending on the local data (see below).** All 34 new tests pass:

| Test class | Tests | Covers |
|---|---|---|
| `UserPaymentMethodTest` | 4 | the expiry month boundary, comparing the year, a missing expiry |
| `UserPaymentMethodDAOIntegrationTest` | 4 | finds your own card; not someone else's, a deleted one or an unknown id |
| `CustomerOrderSavedCardTest` | 17 | each check in the service; Stripe receives exactly `(pi_…, cus_…, pm_…)`; Stripe is never called when a request is refused; a Stripe error leaves the order unchanged; an intent already `succeeded` at Stripe is a 409, an ordinary refusal stays 400 |
| `SavedCardPaymentApiIntegrationTest` | 9 | the endpoint with real login tokens: 204 on success, 403 with no token, 404 for a guest's order, someone else's card or a deleted card, 400 for an expired card, 409 for a paid order (here or already at Stripe), 400 for a missing or empty body |

Stripe is mocked in the backend tests (`@MockitoBean`), and every test rolls back its data.

**Frontend:** `npm run typecheck`, `npm run lint` (0 errors) and `npm run build` are clean. The
existing `e2e/checkout.spec.ts` passes 11/11.

**Playwright: new `e2e/saved-card-checkout.spec.ts`: 7/7**, and it is added to `npm run test:e2e`.
- With a stubbed card list: the primary card is preselected and named on the button; an expired
  card is disabled, labelled and never preselected; "Use a new card" brings back the card form; a
  guest never sees the chooser and never requests the card list.
- Against live Stripe test mode, using test cards saved through our own API: a saved card pays the
  order and our API reports PAID with `visa`/`4242`; a declined card shows the decline and a second
  saved card then pays **the same order**; a 3D Secure card shows the challenge, and completing it
  pays the order.
- The live tests skip when the backend has no Stripe key. Each test deletes the cards it saved,
  which also detaches them at Stripe.
- Three of these tests were run against deliberately broken code (the expiry rule, decline
  handling, and guest card loading). Each one failed, and the code was restored.

**`npm run test:all`: 103 passed, 2 failed, 2 skipped.**

### Failures you will see that this PR did not cause

- **Backend, 3–4 tests; they also fail on `main`:**
  - `CustomerOrderDAOIntegrationTest.filtersByStatus` expects 2 CANCELLED orders and finds 23,
    because earlier Playwright runs left orders in the shared local database.
  - Two or three `ReportServiceImplTest` tests, depending on which orders are in the last 30 days.
    The soft-delete tests pick the order to delete with `findAll()` and no date filter, so on a
    database older than a month they delete a seeded order the 30-day report never counted, and
    the count does not move. (Seed dates are fixed when the Liquibase changeset is applied.)
- **Playwright, 2 tests in `admin.spec.ts`:** the revenue line chart is never drawn. They have the
  same cause: the 30-day window holds only one day of orders, and a line needs two days. This PR
  does not touch reporting.

Details are in `progress_report.md`.

## Not covered

- **A decline followed by a newly typed card on the same order** has only been checked by design,
  not run. An automated browser can't type into Stripe's card form. A decline followed by another
  saved card is covered.
- **Not exercised by any test:** a failed or cancelled 3D Secure challenge, and the "That card is no
  longer available" path (a card deleted in another tab returns 404 and the list reloads).
- **Test data:** each run of the new spec leaves 7 orders in the database (4 `PENDING_PAYMENT`,
  3 `PAID`), because there's no API to delete an order. It also gives `customer@pizza.test` a
  test-mode Stripe Customer the first time a card is saved.

## Follow-ups (not in this PR)

- **Save a card at checkout.** A separate ticket; cards can still only be saved on the profile page.
- **The Angular, React Native and SwiftUI checkouts** don't offer saved cards yet.
- **Make `createOrder`'s Stripe error message match** the saved-card path's generic message.
- **Report tests that age:** each "last 30 days" test should create its own recent order in its
  transaction, instead of relying on the seed data.
- **Review findings deferred:** two tabs choosing different cards on one order (confirm charges the
  card set last: own cards only, never twice); a late card list can swap the payment form; a failed
  reload after a 404 hides its message; the Stripe call sits inside a read-only transaction.
- **Clean up after the Playwright specs:** the orders they leave behind break
  `CustomerOrderDAOIntegrationTest.filtersByStatus`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
