# Customer Data Unification Platform — progress report

## Status: published and live (2026-08-29)

Artifact: https://claude.ai/code/artifact/5ed2f22f-1138-4d95-9892-9f6dc995b2e3
Source: `design.html` in this folder. Republishing that file path keeps the same URL.

Live at **https://lovemesomecoding.com/system-design/system-design-customer-data-platform**
as lesson 14 of the System Design track. The artifact above remains the long-form design; the post
is the track-conforming version of it.

No application code was written — this is a design, in both forms.

---

## The requirement that shaped the design

Of the seven bullets, one is load-bearing: *"can explain why it chose each value."* Every other
requirement has an obvious implementation; that one does not, and the obvious implementations of the
others make it impossible.

So the design is built backwards from it:

> The unified profile is a **pure function over an append-only set of field observations**,
> recomputed on every arrival. Records are never merged into each other.

Two of the stated requirements then stop being features and become properties:

- **Out-of-order events** — a late event just adds a candidate. The function returns the same answer
  regardless of arrival order, so there is no "is this newer than what we have?" check anywhere in
  the flow. (Fig. 3 in the doc draws exactly this difference.)
- **Lineage** — the explanation *is* the candidate set plus the rule that eliminated each loser.
  Nothing has to be logged at decision time for the `/lineage` endpoint to work.

`decision_log` still exists, but for a different question: *what changed and when*, not *why is it
this*. Those are separate structures on purpose.

---

## Decisions worth recording

| Decision | Why |
|---|---|
| Explode records into **one observation per field** | An omitted field produces no row, so partial records stop being destructive. Absence is silence, not a null that overwrites. Clearing needs an explicit tombstone. |
| **Authority tier beats recency**, never the reverse | Recency-wins lets a Support typo overwrite a verified billing address. Recency only competes inside a tier. |
| Tiebreak on **`eventId`**, not the observation row id | A replay from S3 mints new row ids. A row-id tiebreak would let a replay settle on a different value than the original run, which destroys convergence — the one property the whole design rests on. |
| Authority table lives in **`application.yml`**, not code | It is a business decision. `@PostConstruct` fails boot if any canonical field has no authoritative source, because that field would silently lose every value ever sent for it and look exactly like a normalization bug. |
| `record_owner` is the **only mutable link** | A merge rewrites owner rows and nothing else, so `observation` stays honestly append-only and an unmerge is a delete plus a re-resolve. |
| Append an observation **only when the value changed** | Sources re-send whole records constantly. Without this, the table grows with traffic instead of with change — roughly 12× at the sizing in the doc. |
| Losing `customer_id` goes to **`customer_alias`**, never deleted | Downstream systems are holding it. It must keep resolving forever. |
| Weak keys (device, name+postcode, household address) **may attach, never merge** | A shared household address collapsing a family into one person is the classic CDP incident, and it is expensive because every consumer has already acted on it. |
| Outbox row written **in the resolution transaction** | Publishing after commit means a crash between the two leaves a consumer permanently disagreeing with the profile store, undetectably. |
| Ingest split from resolution split from reads | Three unrelated load shapes; one deployable would force them to share a scaling decision. |

### A correction made during the write-up
The first draft of the survivorship rules had "an explicit tombstone wins" as rule 1, ahead of
authority. That is wrong — it lets a low-authority source clear a high-authority value. The rules
and the `SurvivorshipResolver` code now both apply the tombstone check *within the winning tier*,
which is also one comparison shorter.

---

## Deliberately out of scope
Probabilistic / ML matching, real-time streaming segmentation, a self-serve rule builder UI,
cross-device identity. None are needed to satisfy the stated requirements.

GDPR erasure is named but not designed: append-only storage and right-to-erasure genuinely conflict,
and the doc points at crypto-shredding (per-customer data key, erasure = destroy the key) as the
resolution rather than pretending the tension is not there.

---

## Notes
- **A screenshot was pasted with the original request and could not be read** — macOS had already
  deleted its temp copy (`NSIRD_screencaptureui_*`) by the time the tool ran, and it was not on the
  Desktop. The written requirements arrived separately and the design is built from those. If the
  screenshot carried an architecture or constraints, this design has not been reconciled against it.
- No demo app under `lovemesomecoding_demo_project` was used, per instruction — none fits this shape.
- Nothing here is committed.

## Publishing (2026-08-29)
Folau asked to publish it live, with the post dated in 2024. It went into the System Design track
rather than `backend-dev` or `spring-boot`: the content is a system design, and it sits alongside
six sibling "Designing X" case studies.

Placed at **position 14, dated 2024-11-08** — between `chat-system` (2024-09-28) and
`notification-system` (2024-12-19). See `projects/system_design/progress_report.md` for why that
position was the one that let a 2024 date happen without re-dating any published post.

The post is not a copy of `design.html`. The track has its own rules (3,300–4,400 words, 45–88%
prose, ASCII diagrams rather than SVG, `Step N` structure, an interviewer section), so it was
rewritten to them. It came out at 3,367 words, 65% prose, 7 ASCII diagrams.

## Still to do
- [ ] Reconcile against the screenshot if it is re-supplied.
- [ ] Commit — `projects/customer_data_platform/` is untracked and `projects/system_design/` has
      the manifest change plus five renamed files.
