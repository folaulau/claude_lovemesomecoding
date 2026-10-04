# Session 13-review-fixes

mode: `acceptEdits`  cwd: `/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza`  allowed: `Bash(./mvnw:*) Bash(git diff:*) Bash(git status:*) Bash(git log:*)`  resumed: `aa622bee-305d-4a91-bbfa-0b046bb02d30`

## Prompt

```text
A reviewer (who hasn't seen this conversation) reviewed the PR. My decisions on their findings:

ACCEPTED, fix now, each as a separate change I'll commit separately:
(a) If the order's PaymentIntent has already succeeded (paid in another tab, webhook not yet arrived), PUT /payment-method currently turns Stripe's refusal into 400 'That card could not be used... choose another card', inviting the customer to pay again. It should be the 409 'already paid' case instead. Detect it properly (don't string-match Stripe's message if there's a better signal), add a service test and an API test that would fail without the fix.
(b) pizza/CLAUDE.md says every DAOImp wires a repository AND a JdbcTemplate with ReportDAOImp as the one exception. UserPaymentMethodDAOImp is repository-only on purpose. Update the rule text so it is true, in one or two lines. Don't add the field.

DECLINED for this PR (record them as follow-ups in progress_report.md, one line each, nothing else): two tabs choosing different cards on the same order (confirm charges whichever card was set last; own cards only, no double charge); payment form can swap if the card list loads late; failed reload after a 404 hides the message; Stripe call inside the read-only transaction (documented trade-off).

Do (a) first, run spotless and the backend tests, then (b). Don't commit. Summarise and show git status.
```

## Transcript

Starting with (a). First the current service code and the API test as committed (it changed on disk after I wrote it), then the Stripe exception types available, so I can detect "already paid" properly rather than by matching Stripe's message.

- **Bash** command='git log --oneline -1 && git status --short && sed -n 240,266p pizza-springboot-backend/src/main/java/com/pizza/api/entity/order/CustomerOrderServiceImpl.java && grep -n "stripe-java" -A1 pizza-springb'
- **Read** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/SavedCardPaymentApiIntegrationTest.java'
- **Read** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/SavedCardPaymentApiIntegrationTest.java'
- **Bash** command='J=$(ls ~/.m2/repository/com/stripe/stripe-java/*/stripe-java-*.jar | grep -v sources | tail -1); echo "$J"; javap -cp "$J" com.stripe.exception.InvalidRequestException | grep "public com.stripe"; java'
- **Bash** command='ls ~/.m2/repository/com/stripe/stripe-java/'
- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/main/java/com/pizza/api/entity/order/CustomerOrderServiceImpl.java'
`PaymentIntent` is already imported in the service. Now the service test. Reading the end of `CustomerOrderSavedCardTest` as spotless formatted it:

- **Bash** command='grep -n "stripeRefuses\\|^import\\|class CustomerOrderSavedCardTest\\|private static final" pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/CustomerOrderSavedCardTest.java'
- **Read** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/CustomerOrderSavedCardTest.java'
Adding two service tests. The first would fail without the fix. The second makes sure the fix doesn't turn every refusal into a 409:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/CustomerOrderSavedCardTest.java'
- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/CustomerOrderSavedCardTest.java'
Now the API test, which checks the response status a browser would actually get:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/SavedCardPaymentApiIntegrationTest.java'
- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/SavedCardPaymentApiIntegrationTest.java'
- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/test/java/com/pizza/api/entity/order/SavedCardPaymentApiIntegrationTest.java'
Running spotless, then the two test classes with the fix in place:

- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend && ./mvnw -q spotless:apply'
- **Bash** command='./mvnw test -B -Dtest=\'CustomerOrderSavedCardTest,SavedCardPaymentApiIntegrationTest\' 2>&1 | grep -E "Tests run:|<<< FAIL|BUILD|ERROR\\].*\\.java|cannot find symbol|constructor"'
It compiles, so the 6-argument constructor exists, and all 26 pass. To prove the new tests "would fail without the fix", I'll temporarily disable the check and run them:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/main/java/com/pizza/api/entity/order/CustomerOrderServiceImpl.java'
- **Bash** command='./mvnw test -B -Dspotless.check.skip=true -Dtest=\'CustomerOrderSavedCardTest#alreadyPaidAtStripe+refusedButNotPaid,SavedCardPaymentApiIntegrationTest#paidAtStripeButNotYetHere\' 2>&1 | grep -E "Tests r'
Without the fix, both new "already paid" tests fail (`expected:<409> but was:<400>`), and the "not paid → still 400" guard passes as it should. Restoring the fix:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/pizza-springboot-backend/src/main/java/com/pizza/api/entity/order/CustomerOrderServiceImpl.java'
- **Bash** command='./mvnw -q spotless:apply && ./mvnw test -B 2>&1 | grep -E "Tests run:|<<< FAIL|BUILD"'
- **Bash** command='grep -rn "TEMP" src/main/java/com/pizza/api/entity/order/CustomerOrderServiceImpl.java; git status --short'
(a) is complete. Now (b), the DAO rule text in `pizza/CLAUDE.md`:

- **Bash** command='grep -n "Every DAO is\\|implementation wires\\|whichever of the two\\|BalanceDAOImpl.java\\|one exception\\|reporting never loads" ../CLAUDE.md'
- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/CLAUDE.md'
- **Bash** command='sed -n 74,82p ../CLAUDE.md'
- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/CLAUDE.md'
- **Bash** command='git diff ../CLAUDE.md'
Now the four declined findings, one line each, in `progress_report.md`'s "Still open" list after the existing PIZZA-42 follow-ups:

- **Edit** file_path='/Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza/progress_report.md'
- **Bash** command='cd /Users/folaukaveinga/Github/claude_lovemesomecoding/lovemesomecoding_demo_project/pizza && git status --short && git diff --stat'
- **Bash** command='git status --short && git diff --stat'
Both review fixes are made and their tests pass, and the four declined findings are recorded as follow-ups. Nothing is committed. The changes split cleanly into the separate commits you wanted, one group of files each.

## (a) "Already paid" now returns 409, not "choose another card"
**Change:** `CustomerOrderServiceImpl.java`. When Stripe refuses to put the card on the PaymentIntent, the service now asks Stripe for that PaymentIntent's real status, using the existing `stripeService.retrieve`. If the status is `succeeded`, it returns **409 "Order … has already been paid"**. Any other status, or a failed status check, keeps the existing 400.
- **Why this signal:** it's Stripe's own record of the payment, so nothing depends on how Stripe words its error. It's also the same check `refreshPaymentStatus` already uses.
- **Why only after a refusal:** checking first would cost a Stripe round trip on every attempt and could still lose the race.
- **No frontend change needed:** the checkout already shows the server's message for any non-404 error, so the customer now reads "already been paid" and isn't asked to pay again.

**Tests** (3 new):

| Test | With the fix | Fix disabled |
|---|---|---|
| `CustomerOrderSavedCardTest.alreadyPaidAtStripe`: Stripe refuses, the payment has `succeeded` → 409 | pass | **fail**: `expected: 409 CONFLICT` |
| `SavedCardPaymentApiIntegrationTest.paidAtStripeButNotYetHere`: same case through the API, 409 with "already been paid" | pass | **fail**: `Status expected:<409> but was:<400>` |
| `CustomerOrderSavedCardTest.refusedButNotPaid`: Stripe refuses, the payment is still `requires_payment_method` → 400 | pass | pass, as it should |

The third test stops the fix from turning every refusal into a 409. I disabled the check, ran the three tests, then restored the check and confirmed the temporary edit is gone.

**Backend suite** after `spotless:apply`: **94 run, 91 pass**. The 3 failures were already there before PIZZA-42: `filtersByStatus` and two `ReportServiceImplTest` soft-delete tests. `summaryIsInternallyConsistent` passes this time only because today's test orders fall inside its 30-day window, which `progress_report.md` already accounts for ("up to 3").

**Not done:** I didn't treat a `processing` payment as already paid. That status can't be changed either, but it's rare for cards and goes beyond what you accepted. Say if you want it included.

## (b) DAO rule in `pizza/CLAUDE.md`
I changed it in place, keeping the same line count:
- "wires in a Spring Data repository **and** a `JdbcTemplate`" became "a Spring Data repository, a `JdbcTemplate`, or both — whichever its methods need".
- The "one exception" note now names both cases: `ReportDAOImp` is JdbcTemplate-only, and `UserPaymentMethodDAOImp` is repository-only until one of its queries needs SQL.

That's two edits rather than one: leaving the bold **and** would still contradict `UserPaymentMethodDAOImp`. No code changed.

## Declined findings → `progress_report.md`
Four one-line bullets in "Still open", after the existing PIZZA-42 follow-ups:
- two tabs on one order;
- the payment form swapping if the card list loads late;
- the "no longer available" message hidden when the reload also fails;
- the Stripe call inside the read-only transaction.

## git status
```
 M pizza/CLAUDE.md                                                  ← (b)
 M .../order/CustomerOrderServiceImpl.java                          ← (a)
 M .../order/CustomerOrderSavedCardTest.java                        ← (a)
 M .../order/SavedCardPaymentApiIntegrationTest.java                ← (a)
 M pizza/progress_report.md                                         ← declined follow-ups
 5 files changed, 115 insertions(+), 3 deletions(-)
```

**The unsaved PR draft is now out of date.** Its test numbers become **94 backend tests with 34 new**, and two parts need rewriting: the "Stripe refuses → generic 400" decision now needs the 409 exception, and the declined findings may belong under follow-ups. Grant write access to `projects/ai_engineering/sessions/` and I'll save an updated version.


_turns: 29, duration: 188s, cost: $12.31_

## Final answer

Both review fixes are made and their tests pass, and the four declined findings are recorded as follow-ups. Nothing is committed. The changes split cleanly into the separate commits you wanted, one group of files each.

## (a) "Already paid" now returns 409, not "choose another card"
**Change:** `CustomerOrderServiceImpl.java`. When Stripe refuses to put the card on the PaymentIntent, the service now asks Stripe for that PaymentIntent's real status, using the existing `stripeService.retrieve`. If the status is `succeeded`, it returns **409 "Order … has already been paid"**. Any other status, or a failed status check, keeps the existing 400.
- **Why this signal:** it's Stripe's own record of the payment, so nothing depends on how Stripe words its error. It's also the same check `refreshPaymentStatus` already uses.
- **Why only after a refusal:** checking first would cost a Stripe round trip on every attempt and could still lose the race.
- **No frontend change needed:** the checkout already shows the server's message for any non-404 error, so the customer now reads "already been paid" and isn't asked to pay again.

**Tests** (3 new):

| Test | With the fix | Fix disabled |
|---|---|---|
| `CustomerOrderSavedCardTest.alreadyPaidAtStripe`: Stripe refuses, the payment has `succeeded` → 409 | pass | **fail**: `expected: 409 CONFLICT` |
| `SavedCardPaymentApiIntegrationTest.paidAtStripeButNotYetHere`: same case through the API, 409 with "already been paid" | pass | **fail**: `Status expected:<409> but was:<400>` |
| `CustomerOrderSavedCardTest.refusedButNotPaid`: Stripe refuses, the payment is still `requires_payment_method` → 400 | pass | pass, as it should |

The third test stops the fix from turning every refusal into a 409. I disabled the check, ran the three tests, then restored the check and confirmed the temporary edit is gone.

**Backend suite** after `spotless:apply`: **94 run, 91 pass**. The 3 failures were already there before PIZZA-42: `filtersByStatus` and two `ReportServiceImplTest` soft-delete tests. `summaryIsInternallyConsistent` passes this time only because today's test orders fall inside its 30-day window, which `progress_report.md` already accounts for ("up to 3").

**Not done:** I didn't treat a `processing` payment as already paid. That status can't be changed either, but it's rare for cards and goes beyond what you accepted. Say if you want it included.

## (b) DAO rule in `pizza/CLAUDE.md`
I changed it in place, keeping the same line count:
- "wires in a Spring Data repository **and** a `JdbcTemplate`" became "a Spring Data repository, a `JdbcTemplate`, or both — whichever its methods need".
- The "one exception" note now names both cases: `ReportDAOImp` is JdbcTemplate-only, and `UserPaymentMethodDAOImp` is repository-only until one of its queries needs SQL.

That's two edits rather than one: leaving the bold **and** would still contradict `UserPaymentMethodDAOImp`. No code changed.

## Declined findings → `progress_report.md`
Four one-line bullets in "Still open", after the existing PIZZA-42 follow-ups:
- two tabs on one order;
- the payment form swapping if the card list loads late;
- the "no longer available" message hidden when the reload also fails;
- the Stripe call inside the read-only transaction.

## git status
```
 M pizza/CLAUDE.md                                                  ← (b)
 M .../order/CustomerOrderServiceImpl.java                          ← (a)
 M .../order/CustomerOrderSavedCardTest.java                        ← (a)
 M .../order/SavedCardPaymentApiIntegrationTest.java                ← (a)
 M pizza/progress_report.md                                         ← declined follow-ups
 5 files changed, 115 insertions(+), 3 deletions(-)
```

**The unsaved PR draft is now out of date.** Its test numbers become **94 backend tests with 34 new**, and two parts need rewriting: the "Stripe refuses → generic 400" decision now needs the 409 exception, and the declined findings may belong under follow-ups. Grant write access to `projects/ai_engineering/sessions/` and I'll save an updated version.
