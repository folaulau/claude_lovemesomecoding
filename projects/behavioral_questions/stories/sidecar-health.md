# Sidecar Health: provider ratings and reviews

Folau's own account, given 2026-10-27, verbatim. It is the source of record for the worked answer
in `posts/03-behavioral-proudest-project.html`; `check_content.py` checks the figures the post
quotes against this file. Do not add details here that Folau did not supply.

---

Showing doctor ratings and reviews so members can make an educated decision on who to go see.

Sidecar Health is a Health Insurance Provider. Their mission is to reduce Health care costs. What they do is they have their customers pay Health care with cash. By paying with cash the cost of care is about 40% less than the traditional route where the doctor sends a bill to the Insurance company.

For example, as a member if you have a doctor checkup, after you see the doctor. You pull up your Visa debit card provided by Sidecar Health. You then pay for your visit right there and then. You also take a picture of the receipt and upload it to Sidecar Health. And you are done! There is no billing to send from the doctor's office to the insurance company or anything like that. The doctor got his pay already.

At some point members of our platform wanted to see reviews and ratings of doctors near them. Before they would go see a doctor they would like to see how much doctor A is charging for a certain health care service vs doctor B and doctor C. This was something that was not allowed by law at the time. So there was nowhere you could find reviews and ratings of your care provider. Not until the US president at the time signed a bill to force doctors and doctor providers to release their pricing to the public. That was a game changer for us. We have the data to push out. Now the bill just passed and we have customers asking for it.

Our team got together and in a month full of long hours we were able to show ratings and reviews of doctors that our customers or members have visited. This became huge for our members as they could now choose a care provider just like they are choosing their next new TV. There are reviews and ratings to help them make educated decisions. This brought a lot of pride and a smile to my face because there are a lot of people out there that need health care but may think it's too expensive for them. But in reality there are a lot of options and affordable options out there for them.

---

## Editing decisions (2026-10-27)

- "Not allowed by law" is applied to **prices** only. Reviews were never illegal; the transparency
  rules were about publishing prices. An interviewer from healthcare would catch the conflation.
- The law is named generically ("federal price transparency rules"), not as a specific bill,
  until Folau confirms which rule it was.
- Still missing, and asked for: Folau's own part of the build, the hardest problem and the choice
  made, team size, and any result figure. The post does not invent them; it teaches that gap.

## Follow-up answers from Folau (2026-10-27), verbatim

What you owned:
- i owned the backend work.

The hardest problem and how you solved it:
- getting the backend database to be fast enough to do searching. we were using myql 5.7 which did not perform well when we were running fulltext search. we moved the searchable data into elastic search which was a journey by itself. I took the initiative on learning elastic search and having a POC with it and demoing its capabilities to the team. once we decided to use ES we were able clear the performance issue.

Team size and usage:
- 3 people. I was on the backend, 1 QA and 1 frontend dev.
- No usage number given.

Checker spellings recorded here: MySQL 5.7, team of three.
