# Python Advanced track — progress report

**Status:** PUBLISHED — all 8 posts reworked, every gate green, seeded to local and prod, deployed and verified live
**Started:** 2026-08-20
**Where it lands:** https://lovemesomecoding.com/python-advanced

---

## What this is

The continuation of `/python`, which was reworked from 17 posts to 26 earlier the same day
(`projects/python_tutorial/progress_report.md`). `/python-advanced` is eight posts, last touched in
February 2026, and it has the same shape of problem that track had — plus two that are its own.

| | |
|---|---:|
| Posts | 8 |
| Prose words | 15,118 |
| Mean | **1,889 words** — over the 1,800 ceiling |
| Code blocks | 22–**48** per post |
| Reading time | 16–**24 min** |
| `<h2>` per post | 6–**16** (target 4–10), several numbered `1.`…`8.` |
| Tags | 1 (`"python"`) on all 8 |
| `boldgrid` residue | all 8 |
| Category | name lowercase `python-advanced`, description `""` |
| Dates | 2019-03 → 2023-07, scattered |

### Problem one: three posts now duplicate /python

This did not exist before 2026-08-20. Expanding `/python` to 26 posts created it:

| Advanced post | Duplicates |
|---|---|
| `python-advanced-generators-iterators` (37 blocks, 15 h2) | `/python/python-generators-iterators` |
| `python-advanced-map-reduce-and-filter` | `/python/python-lambda-functions` — which already argues map/filter lose to comprehensions |
| `python-advanced-virtual-environments-pip` (48 blocks) | `/python/python-get-started` and `/python/python-modules-packages`, which both cover venv, pip and requirements.txt |

Near-duplicate content on the same site means Google picks one of the pair for you, and a reader who
follows the track in order reads the same explanation twice.

### Problem two: half the track is about libraries the checker could not run

`/python`'s guarantee was that every code block is executed and every `# Output:` claim verified —
456 of them. That guarantee does not survive contact with this track by default:

| Package | 3.12 | 3.14 |
|---|---|---|
| numpy, pandas, matplotlib, yaml, mysql-connector, requests | installed | **absent** |
| scikit-learn, marshmallow, sqlalchemy, pytest | **absent** | **absent** |

The checker runs every block under both interpreters, so a NumPy block fails on 3.14 regardless of
whether the sample is correct. Marking them all `norun` would have left **four of the eight posts
unverified** — and the MySQL and machine learning posts are precisely where a stale API call hides.

## Decisions

All three taken by Folau on 2026-08-20.

| Decision | Choice | Why |
|---|---|---|
| The three overlapping posts | **Repoint deeper, keep every slug** | All indexed since 2019–2021. Redirecting them away would waste three ranking URLs; leaving them would ship duplicate content. |
| Third-party snippets | **Dedicated venv, 3.12 only** | Keeps the run-and-verify guarantee on the four library posts. See below. |
| Track size | **8 — rework all, add none** | Get it correct and consistent with `/python` first. |
| Existing 8 slugs | **Keep every one** | `manifest.EXISTING_SLUGS` makes adding or dropping one a hard error, not just a convention. |
| Length | **900–1,800 words**, `CODE_BLOCK_MAX = 14`, 4–10 `<h2>` | Same gates as `/python`. |
| Tags | **4 per post** | Currently one, the literal string `"python"`. |
| `boldgrid` divs | **Strip entirely** | Migration residue. |
| Dates | **Restamp 2026-08-05 … 2026-08-19, 2 days apart, at 15:00** | 15:00 was the free hour — see the manifest docstring. |
| Publish | **Seed local → prod → deploy** | Same flow as `/python`. |

### Repointing, not redirecting

Each of the three keeps its URL and title-level topic but now starts where `/python` stops.
`manifest.OVERLAP` is the source of truth so the boundary does not erode the next time either track
is edited:

| Slug | Now covers | Defers to /python |
|---|---|---|
| `…generators-iterators` | The iterator protocol by hand, generators as coroutines (`send`/`throw`/`close`), `contextlib`, `itertools` beyond the basics | What `yield` is, why laziness matters |
| `…map-reduce-and-filter` | `functools` — `reduce`, `partial`, `cache`, `singledispatch` — and the `operator` module | Lambda syntax, why a comprehension beats `map`/`filter` |
| `…virtual-environments-pip` | Packaging: `pyproject.toml`, editable installs, lockfiles, publishing to PyPI | Creating a venv, activating it, `pip install` |

The third is retitled **Packaging & Publishing**. Its slug still says `virtual-environments-pip`,
which is a small mismatch and the right trade — the URL is indexed and the content is what a reader
arriving from that search actually needs next.

### The verification venv

`projects/python_advanced/.venv`, built from a **pinned** `requirements-check.txt`. A block marked
`<!-- needs: numpy -->` runs there, under 3.12 only; pure-stdlib blocks still run under both 3.12
and 3.14.

Pinned deliberately: an unpinned upgrade would silently change what the posts are verified against,
which is the same class of problem as the posts going stale in the first place.

**The marker is mandatory, and that took a second pass to get right.** The first version relied on
the two-interpreter rule to catch a missing marker — a NumPy block without one fails on 3.14, where
NumPy is absent. Testing showed it *passed* on bare 3.12, because NumPy is in that interpreter's own
site-packages rather than the user site-packages `-s` excludes. So the protection was incidental:
install NumPy for 3.14 and a missing marker starts passing silently. `check_snippets.py` now reads
the imports of every block and refuses an unmarked one that imports anything in
`manifest.THIRD_PARTY` — and equally refuses a `needs:` marker naming a package the block never
imports, so the markers cannot rot in the other direction either.

## Reading order

| # | Slug | Was (words / blocks) | Date |
|---|------|---:|------|
| | **Language depth** | | |
| 1 | `python-advanced-generators-iterators` **(repointed)** | 1,624 / 37 | 2026-08-05 |
| 2 | `python-advanced-map-reduce-and-filter` **(repointed)** | 1,556 / 35 | 2026-08-07 |
| 3 | `python-advanced-serialization` | 1,498 / 25 | 2026-08-09 |
| | **Shipping it** | | |
| 4 | `python-advanced-virtual-environments-pip` **(repointed)** | 2,592 / **48** | 2026-08-11 |
| | **Data** | | |
| 5 | `python-advanced-numpy-arrays` | 1,210 / 37 | 2026-08-13 |
| 6 | `python-advanced-mysql` | 1,810 / 34 | 2026-08-15 |
| 7 | `python-advanced-machine-learning` | 2,084 / 22 | 2026-08-17 |
| | **Interviews** | | |
| 8 | `python-advanced-interview-questions` | 2,744 / 27 | 2026-08-19 |

## Files

```
projects/python_advanced/
  README.md                 the requirements and the scope note
  progress_report.md        this file
  manifest.py               category metadata, OVERLAP boundary, THIRD_PARTY set, one entry per post
  requirements-check.txt    pinned deps for the verification venv
  .venv/                    built from the above; gitignored
  posts/NN-slug.html        post bodies
  seed.py                   writes the posts into a content tree
  check_content.py          normaliser round-trip + word/code-block/heading/tag gates
  check_snippets.py         RUNS every block; third-party ones in .venv under 3.12
  check_provenance.py       proves every `<!-- from: -->` block is really in the demo app
  check_links.py            HTML well-formedness + every internal link resolves
  check.sh                  runs all of the above
```

Adapted from `projects/python_tutorial/`. The `needs:` marker and the venv runner are new.

```bash
./projects/python_advanced/check.sh            # offline gates
./projects/python_advanced/check.sh --links    # + the S3-backed link check
python3 projects/python_advanced/seed.py --env local --write --force-dates
```

## Result

| | Before | After |
|---|---:|---:|
| Posts | 8 | 8 (all reworked, none added or dropped) |
| Prose words, mean | 1,889 | 998 |
| Code blocks per post | 22–**48** | 1–8 (cap 14) |
| `<h2>` per post | 6–**16** | 7–9 |
| Numbered `1.`…`8.` headings | 3 posts | 0 |
| Tags per post | 1 | 4 |
| `boldgrid` residue | all 8 | 0 |
| Category name / description | `python-advanced` / empty | `Python Advanced` / written |
| Dates | 2019-03 → 2023-07, scattered | 2026-08-05 → 08-19, teaching order |
| Verified code samples | 0 | **49 blocks, 84 runs, 123 output claims** |
| — of which run in the venv | — | **14 blocks** across NumPy, ML and YAML |

`python-advanced-virtual-environments-pip` went from 48 code blocks to 8; `…numpy-arrays` from 37 to
7; `…generators-iterators` from 37 to 8.

Live and confirmed: `/python-advanced` lists 8 posts in reading order, all eight original URLs
resolve 200, and the packaging post serves the new content (`pyproject.toml` present, the old
"Activating and Deactivating" section gone).

## What the checkers caught

| Post | Caught |
|---|---|
| `…map-reduce-and-filter` | I claimed a dict merge produced `{'a': 1, 'b': 2, 'a': 99}` — **a dict cannot have duplicate keys**. Real output `{'a': 99, 'b': 2}`, which is now a teaching point about precedence and key position. |
| `…serialization` | A PyYAML block with no `needs:` marker. Caught by the mandatory-marker check, not by luck. |
| `…numpy-arrays` | NumPy's exact repr spacing — `[ 90. 225.  36.]`, not what I wrote. |
| `…mysql` | `cursor.rowcount` after a `SELECT` is `-1`, not `>= 0`. Replaced with `cursor.description`, and the post now says why. |
| `…machine-learning` | Feature importances differ depending on whether the model was fit on the split or the full set — my prose said petal *width* from one run while the block computed petal *length* from another. |

The machine learning numbers were produced by **running the example first and reading the output**,
rather than writing plausible figures and hoping. Accuracy 0.889, the confusion matrix, and the
five cross-validation scores are all real.

## Open questions

None. All three scoping decisions answered by Folau on 2026-08-20.

The `.venv` is gitignored and rebuildable from `requirements-check.txt`; a missing one is reported
as a failure by `check_snippets.py` rather than silently skipping the third-party blocks.

## Log

| Date | What |
|---|---|
| 2026-08-20 | Audited `/python-advanced`: 8 posts, 1,889 mean words, 22–48 code blocks, 6–16 h2, 1 tag each, boldgrid on all 8, category name and description unset. |
| 2026-08-20 | Found the overlap created hours earlier by expanding `/python` to 26 posts — three of the eight now duplicated it. |
| 2026-08-20 | Measured third-party availability rather than assuming it: four packages absent from both interpreters, six absent from 3.14. |
| 2026-08-20 | Folau: repoint the three, build a pinned venv for third-party verification, keep the track at 8. |
| 2026-08-20 | Scaffolded. Tested the `needs:` runner with a deliberately broken fixture, found the marker was only incidentally enforced, and made it mandatory in both directions. |
| 2026-08-20 | Reworked all eight posts. Five caught errors, recorded above. |
| 2026-08-20 | All gates green: 49 blocks / 84 runs / 123 output claims, 14 of them in the venv; 20 internal links resolve; build guard 603/603 posts and 44/44 category counts. |
| 2026-08-20 | Seeded local then prod, deployed, invalidated CloudFront and verified the live pages serve the new content. |
