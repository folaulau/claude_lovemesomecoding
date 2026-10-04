# Session 05-requirements

mode: `plan`  cwd: `/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza`  resumed: `aa622bee-305d-4a91-bbfa-0b046bb02d30`

## Prompt

```text
Here's the ticket as the product owner wrote it:

  PIZZA-42: As a signed-in customer, I want to pay with one of my saved cards at checkout so I don't have to type my card every time.

That's all it says. Using what you found in the code, don't plan or write anything yet. Instead:
1. List the questions I need answered by the product owner before this is buildable. Only questions whose answer changes what we build.
2. List the edge cases and failure modes this has to handle.
3. Flag anything in the ticket that conflicts with how the app already behaves.
For each question, say what you'd assume if nobody answers, so I can see your defaults.
```

## Transcript

- **Bash** command='grep -n -i "checkout\\|primary\\|expir" pizza-react-frontend/src/pages/ProfilePage.tsx | sed -n 1,40p; grep -rn -i "saved card\\|paymentMethod\\|customerEphemeral\\|ephemeral" pizza-react-native-mobile/src'
Nothing is planned or written yet; all of this comes from the code I traced earlier. One question matters more than the rest: today a card can only be saved from the profile page, so a customer who never goes there will still type their card every time, even after this ticket ships.

## 1. Questions for the product owner

Each one changes what gets built. The default is what I'd assume if nobody answers.

| # | Question | Why it changes the build | Default |
|---|---|---|---|
| Q1 | **When someone pays with a new card at checkout, should they be offered "Save this card for next time"?** | Today a card can only be saved on the profile page (`ProfilePage.tsx:178-186`, `UserProfileServiceImpl.java:147-211`). Saving at checkout needs the intent to carry the Stripe Customer and be marked for reuse, plus a way to record the card after payment. That roughly doubles the backend work. | **Out of scope; raise it as a separate ticket.** Ask the PO directly, because their "so I don't have to type my card" depends on it. |
| Q2 | **Is the primary card preselected?** | Decides whether checkout defaults to a saved card or to "new card". | **Yes, the primary is preselected, with "Use a new card" as the last option**, the same as the address chooser (`CheckoutPage.tsx:70-96`, `:339-372`). |
| Q3 | **Where does the customer choose the card: on the details step, or on the payment step after "Continue to payment"?** | Choosing on the details step lets the card be fixed when the order is created (simplest). Choosing on the payment step, or switching cards after a decline, means changing the existing payment after the order exists. That needs an update endpoint, because the order's Stripe request key can't be reused with different parameters (`StripeService.java:100-101`). | **The payment step**, where paying happens today. Q5's decline fallback needs card switching anyway, so the update path gets built either way. |
| Q4 | **What happens to expired cards?** | Expiry is already stored (`UserPaymentMethod.java:77-81`) and shown (`ProfilePage.tsx:378`), so this is a filter or a disabled state. | **Shown but disabled, labelled "Expired"**, so the customer understands why their card isn't selectable. |
| Q5 | **If a saved card is declined or fails 3D Secure, what can the customer do?** | Retrying on the same order means the payment can't be locked to one card at order creation. Starting over means a new order and a new abandoned `PENDING_PAYMENT` row. | **Show the decline and let them pick another saved card or enter a new one on the same order.** |
| Q6 | **Must the customer re-enter the CVC for a saved card?** | Stripe supports asking for the CVC again; it adds a Stripe-hosted field and changes how payment is confirmed. | **No**, which matches the ticket's "don't have to type my card". |
| Q7 | **One click, or an explicit confirm?** | Paying immediately on selection vs a "Pay $X with Visa ••4242" button. | **An explicit button showing the card and the server's total.** |
| Q8 | **Which apps does this cover?** | `CLAUDE.md` lists the saved-card gap as open for all four frontends, and the two web apps and two mobile apps are each meant to be the same product. React-only makes the Angular app diverge. The mobile apps use Stripe's PaymentSheet, which handles saved cards differently (`pizza-react-native-mobile/src/features/checkout/payment/paymentGateway.tsx:18`). | **Backend + React only, as you scoped it.** The backend is written so Angular can use it unchanged, and the divergence is recorded in `progress_report.md`. |
| Q9 | **Can customers add, delete or change their primary card from checkout?** | Adds profile-style card management to checkout. | **No; that stays on the profile page.** |

## 2. Edge cases and failure modes

**Ownership and identity**
- **A guest sends a saved-card id.** Placing an order is open to guests (`SecurityConfig.java:117-118`). This should be rejected with 400, not ignored. The current guest path must stay exactly as it is.
- **Someone else's card id.** Return **404, not 403**, the same rule as `requireOwnedPaymentMethod` (`UserProfileServiceImpl.java:264-282`).
- **A card deleted in another tab** between the list loading and Pay. Soft-deleted rows disappear from lookups (`UserPaymentMethod.java:42`), so the request returns 404. The UI should say the card is no longer available and reload the list.
- **The sign-in expires on the payment step.** The order already exists. If changing the card needs sign-in, it fails partway; this needs a clear message rather than a stuck page.

**Stripe state drifting from our database**
- **A card we still list is no longer usable at Stripe**, for example removed in the Stripe dashboard. Stripe errors when the payment is created or confirmed. Show a message telling the customer to choose another card.
- **The Stripe secret key is replaced by one from a different Stripe account.** `CLAUDE.md` says the current key is burned and must be rolled. A new key in the *same* account is fine. A key from a different sandbox makes every stored customer id and card id fail with "No such customer". This is most likely to hit local dev.
- **Stripe isn't configured.** No `clientSecret` comes back (`CustomerOrderServiceImpl.java:87-101`). The saved-card path needs the same clear warning that `CheckoutPage.tsx:230-237` shows.

**Payment outcomes**
- **3D Secure required** (Stripe test card `4000 0025 0000 3155`). The payment is left waiting for authentication. Confirmation has to stay in the browser so Stripe.js can show the challenge; a server-only charge would just fail.
- **Declined at charge time** (test card `4000 0000 0000 0341` saves fine, then declines). This is the realistic test for Q5.
- **Double-clicking Pay.** Disable the button, as `StripePaymentForm.tsx:85` does. Stripe also refuses to confirm the same payment twice.
- **Switching from a saved card to a new card** after the payment already has the saved card on it. The new card from Stripe's form must override it, otherwise the saved card gets charged.
- **Payment succeeds but neither the webhook nor polling sees it in time.** This exists today: polling gives up after 10 tries (`OrderConfirmationPage.tsx:17-18`). Marking an order paid is already safe to repeat (`CustomerOrderServiceImpl.java:176-178`). Nothing new to do, but the saved-card path must keep going through the same mechanism.
- **The confirmation page's "Paid with" line.** `captureCardDetails` reads it back from Stripe (`CustomerOrderServiceImpl.java:207-238`), so it should just work. It's worth one test asserting "Visa ending 4242" after a saved-card payment.

**Data**
- **Missing brand or last4.** In theory it can be null (`UserProfileServiceImpl.java:190-193`), though saving is limited to cards (`StripeService.java:160`). The chooser shouldn't render "null ending null".
- **Refreshing on the payment step** loses the created order (component state at `CheckoutPage.tsx:38`) and creates a new one on resubmit. That's existing behaviour, not new, but saved-card retries will make it more visible.

## 3. Where the ticket conflicts with the app

1. **"So I don't have to type my card every time" assumes the card is already saved,** but the only way to save one is the profile page (see Q1). A customer who never visits it gets nothing from this ticket. The PO may think saving at checkout is included.
2. **The app already promises a default card at checkout and doesn't deliver it.** The API docs for setting a primary card say "Make this the card selected by default at checkout" (`UserProfileRestController.java:98`), and the profile page labels a primary card. The ticket doesn't mention defaults, but the existing behaviour has effectively answered Q2. Confirm it rather than leaving it implicit.
3. **Checkout is two steps, and paying happens after the order exists** (`CheckoutPage.tsx:14-26`). "Pay with one of my saved cards" reads like a single action. Choosing a card can't happen any earlier than the order (Q3); a true one-step checkout would be a bigger redesign the ticket doesn't ask for.
4. **The apps are meant to be the same product** (`CLAUDE.md`: the web apps are "deliberately the same app"; the "Still open" note covers "all four" frontends). A React-only ticket breaks that on purpose. That's fine if the PO accepts it, but they should know the Angular app will lag.
5. **The ticket doesn't mention guests.** It says "signed-in", which fits, but guest checkout must stay unchanged and guests must not be able to send a card id (`CLAUDE.md`: "Guest checkout works end to end").


_turns: 2, duration: 62s, cost: $1.27_

## Final answer

Nothing is planned or written yet; all of this comes from the code I traced earlier. One question matters more than the rest: today a card can only be saved from the profile page, so a customer who never goes there will still type their card every time, even after this ticket ships.

## 1. Questions for the product owner

Each one changes what gets built. The default is what I'd assume if nobody answers.

| # | Question | Why it changes the build | Default |
|---|---|---|---|
| Q1 | **When someone pays with a new card at checkout, should they be offered "Save this card for next time"?** | Today a card can only be saved on the profile page (`ProfilePage.tsx:178-186`, `UserProfileServiceImpl.java:147-211`). Saving at checkout needs the intent to carry the Stripe Customer and be marked for reuse, plus a way to record the card after payment. That roughly doubles the backend work. | **Out of scope; raise it as a separate ticket.** Ask the PO directly, because their "so I don't have to type my card" depends on it. |
| Q2 | **Is the primary card preselected?** | Decides whether checkout defaults to a saved card or to "new card". | **Yes, the primary is preselected, with "Use a new card" as the last option**, the same as the address chooser (`CheckoutPage.tsx:70-96`, `:339-372`). |
| Q3 | **Where does the customer choose the card: on the details step, or on the payment step after "Continue to payment"?** | Choosing on the details step lets the card be fixed when the order is created (simplest). Choosing on the payment step, or switching cards after a decline, means changing the existing payment after the order exists. That needs an update endpoint, because the order's Stripe request key can't be reused with different parameters (`StripeService.java:100-101`). | **The payment step**, where paying happens today. Q5's decline fallback needs card switching anyway, so the update path gets built either way. |
| Q4 | **What happens to expired cards?** | Expiry is already stored (`UserPaymentMethod.java:77-81`) and shown (`ProfilePage.tsx:378`), so this is a filter or a disabled state. | **Shown but disabled, labelled "Expired"**, so the customer understands why their card isn't selectable. |
| Q5 | **If a saved card is declined or fails 3D Secure, what can the customer do?** | Retrying on the same order means the payment can't be locked to one card at order creation. Starting over means a new order and a new abandoned `PENDING_PAYMENT` row. | **Show the decline and let them pick another saved card or enter a new one on the same order.** |
| Q6 | **Must the customer re-enter the CVC for a saved card?** | Stripe supports asking for the CVC again; it adds a Stripe-hosted field and changes how payment is confirmed. | **No**, which matches the ticket's "don't have to type my card". |
| Q7 | **One click, or an explicit confirm?** | Paying immediately on selection vs a "Pay $X with Visa ••4242" button. | **An explicit button showing the card and the server's total.** |
| Q8 | **Which apps does this cover?** | `CLAUDE.md` lists the saved-card gap as open for all four frontends, and the two web apps and two mobile apps are each meant to be the same product. React-only makes the Angular app diverge. The mobile apps use Stripe's PaymentSheet, which handles saved cards differently (`pizza-react-native-mobile/src/features/checkout/payment/paymentGateway.tsx:18`). | **Backend + React only, as you scoped it.** The backend is written so Angular can use it unchanged, and the divergence is recorded in `progress_report.md`. |
| Q9 | **Can customers add, delete or change their primary card from checkout?** | Adds profile-style card management to checkout. | **No; that stays on the profile page.** |

## 2. Edge cases and failure modes

**Ownership and identity**
- **A guest sends a saved-card id.** Placing an order is open to guests (`SecurityConfig.java:117-118`). This should be rejected with 400, not ignored. The current guest path must stay exactly as it is.
- **Someone else's card id.** Return **404, not 403**, the same rule as `requireOwnedPaymentMethod` (`UserProfileServiceImpl.java:264-282`).
- **A card deleted in another tab** between the list loading and Pay. Soft-deleted rows disappear from lookups (`UserPaymentMethod.java:42`), so the request returns 404. The UI should say the card is no longer available and reload the list.
- **The sign-in expires on the payment step.** The order already exists. If changing the card needs sign-in, it fails partway; this needs a clear message rather than a stuck page.

**Stripe state drifting from our database**
- **A card we still list is no longer usable at Stripe**, for example removed in the Stripe dashboard. Stripe errors when the payment is created or confirmed. Show a message telling the customer to choose another card.
- **The Stripe secret key is replaced by one from a different Stripe account.** `CLAUDE.md` says the current key is burned and must be rolled. A new key in the *same* account is fine. A key from a different sandbox makes every stored customer id and card id fail with "No such customer". This is most likely to hit local dev.
- **Stripe isn't configured.** No `clientSecret` comes back (`CustomerOrderServiceImpl.java:87-101`). The saved-card path needs the same clear warning that `CheckoutPage.tsx:230-237` shows.

**Payment outcomes**
- **3D Secure required** (Stripe test card `4000 0025 0000 3155`). The payment is left waiting for authentication. Confirmation has to stay in the browser so Stripe.js can show the challenge; a server-only charge would just fail.
- **Declined at charge time** (test card `4000 0000 0000 0341` saves fine, then declines). This is the realistic test for Q5.
- **Double-clicking Pay.** Disable the button, as `StripePaymentForm.tsx:85` does. Stripe also refuses to confirm the same payment twice.
- **Switching from a saved card to a new card** after the payment already has the saved card on it. The new card from Stripe's form must override it, otherwise the saved card gets charged.
- **Payment succeeds but neither the webhook nor polling sees it in time.** This exists today: polling gives up after 10 tries (`OrderConfirmationPage.tsx:17-18`). Marking an order paid is already safe to repeat (`CustomerOrderServiceImpl.java:176-178`). Nothing new to do, but the saved-card path must keep going through the same mechanism.
- **The confirmation page's "Paid with" line.** `captureCardDetails` reads it back from Stripe (`CustomerOrderServiceImpl.java:207-238`), so it should just work. It's worth one test asserting "Visa ending 4242" after a saved-card payment.

**Data**
- **Missing brand or last4.** In theory it can be null (`UserProfileServiceImpl.java:190-193`), though saving is limited to cards (`StripeService.java:160`). The chooser shouldn't render "null ending null".
- **Refreshing on the payment step** loses the created order (component state at `CheckoutPage.tsx:38`) and creates a new one on resubmit. That's existing behaviour, not new, but saved-card retries will make it more visible.

## 3. Where the ticket conflicts with the app

1. **"So I don't have to type my card every time" assumes the card is already saved,** but the only way to save one is the profile page (see Q1). A customer who never visits it gets nothing from this ticket. The PO may think saving at checkout is included.
2. **The app already promises a default card at checkout and doesn't deliver it.** The API docs for setting a primary card say "Make this the card selected by default at checkout" (`UserProfileRestController.java:98`), and the profile page labels a primary card. The ticket doesn't mention defaults, but the existing behaviour has effectively answered Q2. Confirm it rather than leaving it implicit.
3. **Checkout is two steps, and paying happens after the order exists** (`CheckoutPage.tsx:14-26`). "Pay with one of my saved cards" reads like a single action. Choosing a card can't happen any earlier than the order (Q3); a true one-step checkout would be a bigger redesign the ticket doesn't ask for.
4. **The apps are meant to be the same product** (`CLAUDE.md`: the web apps are "deliberately the same app"; the "Still open" note covers "all four" frontends). A React-only ticket breaks that on purpose. That's fine if the PO accepts it, but they should know the Angular app will lag.
5. **The ticket doesn't mention guests.** It says "signed-in", which fits, but guest checkout must stay unchanged and guests must not be able to send a card id (`CLAUDE.md`: "Guest checkout works end to end").
