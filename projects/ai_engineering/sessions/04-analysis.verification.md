# Verifying session 04 (the engineer's check, done by hand against the code)

| Claim | Checked | Result |
|---|---|---|
| PaymentIntent created with no `customer` — StripeService.java:82-90 | read lines 68-105 | ✅ true; builder sets amount, currency, metadata, automatic PMs only |
| Idempotency key `order-<uuid>` — :100-101 | same | ✅ true |
| Ownership check is private `requireOwnedPaymentMethod`, 404 not 403 — UserProfileServiceImpl:264-282 | read 260-285 | ✅ true (method at ~276; Javadoc on the address twin explains the 404) |
| `@SQLRestriction` hides deleted cards — UserPaymentMethod.java:42 | read 40-46 | ✅ true, line 42 exactly |
| progress_report.md:1063 and :1504 say checkout doesn't offer saved cards | sed | ✅ true |
| `OrderCreateRequest` at types/index.ts:146 | sed 140-150 | ✅ true |
| Pay button at CheckoutPage.tsx:494-512 | sed | ✅ true |
| OrderApiIntegrationTest mocks StripeService | sed 43-49 | ✅ true, BUT it stubs `isConfigured() -> false` |

⚠️ Nuance the session did not flag: because the test stubs `isConfigured()` to false, the order
service skips Stripe entirely. Its suggested test "own card -> customer and card reach Stripe" will
not exercise Stripe unless that test re-stubs `isConfigured()` to true. Watch for this in post 8.

Also notable for post 2/15: plan mode wrote a plan file OUTSIDE the repo
(~/.claude-personal/plans/...). "Don't change any files" was honoured for the repo.
