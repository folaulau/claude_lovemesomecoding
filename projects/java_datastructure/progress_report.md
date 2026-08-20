# Java Data Structures track — progress report

**Status:** PUBLISHED — live on prod, 2026-08-18
**Started:** 2026-08-18
**Where it lands:** https://lovemesomecoding.com/data-structure-algorithm

---

## What this is

`/data-structure-algorithm` holds **24 posts published 2018–2019**. It is the thinnest track on the
site — **16,756 words in total**, median ~700 — and partly broken:

| Problem | Detail |
|---|---|
| **3 posts are completely empty** | `merge-sort`, `breadth-first-search`, `depth-first-search` — `wordCount: 0`, ~155 bytes each |
| **6 more are stubs** | `introduction` (116 w), `graph` (147), `omega` (155), `trie` (224), `greedy-algorithms` (378), `arraylist` (446) |
| **41 of 50 code blocks are `language-plaintext`** | No syntax highlighting anywhere except 9 blocks |
| **Only 3 of 24 posts use `<h2>`** | So almost none has working heading anchors |

This project rewrites all 24 **in place** — same slugs, so no indexed URL is lost — against
**Java 25**, and adds a landing page. **Result: a 25-post track.**

### ⚠️ Four inbound links constrain this

The LeetCode track already links into this one, and `fundamental-problem-recursion` deliberately
does *not* re-explain recursion because this track's post does. Breaking these would break the
other track's editorial design, not merely a URL:

| Target here | Linked from |
|---|---|
| `data-structure-algorithm-binary-search` | `fundamental-problem/fundamental-problem-binary-search` |
| `data-structure-algorithm-quick-sort` | `fundamental-problem/fundamental-problem-quick-sort` |
| `data-structure-algorithm-recursion` | `fundamental-problem/fundamental-problem-nth-fibonacci` |
| `data-structure-algorithm-recursion` | `fundamental-problem/fundamental-problem-recursion` |

All three slugs are kept, and the rewrites stay compatible with what the other track says about
them.

## Decisions

| Decision | Choice | Why |
|---|---|---|
| Java version | **Java 25 LTS** | The current LTS (Sept 2025) and installed here, so every sample is actually compiled and run. Java 21 would match the other tracks but is a stretch for "the latest version of Java". Folau, 2026-08-18. |
| Track size | **25** — 24 rewritten + 1 landing page | Keeps every indexed URL and every inbound link. |
| Existing 24 | Rewrite in place, keep every slug | See the table above. |
| Code verification | **Compile AND run every sample** | Folau's call. For an algorithms track this is the whole credibility of the content — a published binary search with an off-by-one is worse than no post. |
| Snippet source | **Real `.java` files in `src/dsa/`** | There is no demo app for this domain, so the sources *are* the demo app. `check_content.py` fails if a published snippet and its source have drifted apart. |
| Publish | **Seed local → Folau reviews → prod** | Folau's call. |
| Sibling categories | Out of scope | `java` (28), `java-8` (36), `fundamental-problem` (44), `algorithm-interview` (1) are separate. The README names `/data-structure-algorithm` only. |

### Why real source files rather than snippets in the HTML

The `/spring-boot` and `/spring-study-guide` tracks got "provably compiling code" for free by
lifting every snippet from the pizza demo app. There is no equivalent app for data structures, so
this track builds one: `src/dsa/` holds the implementations, `tests/run.sh` compiles them with
`-Werror` and runs the assertions, and the posts quote from them.

`projects/leetcode/tests/build_java.py` does the opposite — it extracts Java *out of* the published
HTML and hand-wires a `Main.java`, one line per post, and that file is now 51 KB of maintenance.
Going source-first inverts it: the code is a normal Java project that an editor can check, and the
posts are downstream of it.

## Versions

| | |
|---|---|
| Java | **25** (Corretto 25.0.0, LTS, Sept 2025) |
| Build | none — `javac` and `java`, no dependencies |
| Tests | none — a 40-line `Check` harness, so `tests/run.sh` works on a clean machine |

## The Java sources — all green

`tests/run.sh` → **261 assertions, 0 failures**, clean compile under `-Xlint:all -Werror`.

| File | Covers | Notable case asserted |
|---|---|---|
| `Check.java` | the test harness | — |
| `DynamicArray.java` | array, arraylist | doubling vs +1 growth; 1 → 1024 in ten doublings |
| `SinglyLinkedList.java` | linked-list | reverse fixes the tail; Floyd cycle detection |
| `ArrayStack.java` | stack | balanced brackets, including `")("` and unclosed |
| `ArrayQueue.java` | queue | **grow while wrapped** — the bug small tests never hit |
| `HashTable.java` | hashtable | `floorMod` for negative hashCodes; 200 keys survive rehash |
| `Searching.java` | binary-search | overflow of `(low+high)/2` proved arithmetically; `lowerBound` |
| `Sorting.java` | merge-sort, quick-sort | 100k sorted input does not overflow the stack |
| `BinarySearchTree.java` | trees | delete with 0/1/2 children; sorted input degenerates to height 10 |
| `MinHeap.java` | heap, priority-queue | `heapify` is O(n); k-smallest |
| `Trie.java` | trie | prefix ≠ word; digits and punctuation |
| `Graph.java` | graph, BFS, DFS | cycles terminate; directed edges are one-way |
| `Recursion.java` | recursion | Hanoi is 2^n − 1; a million frames really does overflow |
| `DivideAndConquer.java` | divide-and-conquer | inversion count cross-checked against brute force |
| `DynamicProgramming.java` | dynamic-programming | coin change {1,3,4}/6 — where greedy is wrong |
| `Greedy.java` | greedy-algorithms | the same case, showing greedy losing to DP |
| `JdkCollections.java` | the standard-library counterparts | `PriorityQueue` does not iterate sorted; `binarySearch` miss decoding |

The last two are deliberately paired: greedy returning 3 coins where DP returns 2 is asserted in
both files, so the two posts cannot drift apart on the one example that matters.

## Topic list

Reading order. `date` ascends with the track so the prev/next pager reads 1 → 25.
Dates run 2026-07-01 … 2026-08-18, two days apart, at **10:00** — the other tracks stamp 09:00
(`/spring-boot`) and 14:00 (`/spring-study-guide`), and an exact tie leaves archive order to sort
stability.

| # | Slug | State | Backed by |
|---|------|-------|-----------|
| 1 | `data-structure-algorithm-get-started` | **new** | — |
| 2 | `data-structure-algorithm-introduction` | rewrite (116 w) | — |
| 3 | `data-structure-algorithm-memory` | rewrite | — |
| 4 | `data-structure-algorithm-big-o-notation` | rewrite | — |
| 5 | `data-structure-algorithm-omega` | rewrite (155 w) | — |
| 6 | `data-structure-algorithm-array` | rewrite | `DynamicArray` |
| 7 | `data-structure-algorithm-arraylist` | rewrite (446 w) | `DynamicArray` |
| 8 | `data-structure-algorithm-linked-list` | rewrite | `SinglyLinkedList` |
| 9 | `data-structure-algorithm-stack` | rewrite | `ArrayStack` |
| 10 | `data-structure-algorithm-queue` | rewrite | `ArrayQueue` |
| 11 | `data-structure-algorithm-hashtable` | rewrite | `HashTable` |
| 12 | `data-structure-algorithm-recursion` | rewrite | `Recursion` |
| 13 | `data-structure-algorithm-divide-and-conquer` | rewrite | `DivideAndConquer` |
| 14 | `data-structure-algorithm-dynamic-programming` | rewrite | `DynamicProgramming` |
| 15 | `data-structure-algorithm-greedy-algorithms` | rewrite (378 w) | `Greedy` |
| 16 | `data-structure-algorithm-binary-search` | rewrite | `Searching` |
| 17 | `data-structure-algorithm-merge-sort` | rewrite (**empty**) | `Sorting` |
| 18 | `data-structure-algorithm-quick-sort` | rewrite | `Sorting` |
| 19 | `data-structure-algorithm-trees` | rewrite | `BinarySearchTree` |
| 20 | `data-structure-algorithm-heap` | rewrite | `MinHeap` |
| 21 | `data-structure-algorithm-priority-queue` | rewrite | `MinHeap` |
| 22 | `data-structure-algorithm-trie` | rewrite (224 w) | `Trie` |
| 23 | `data-structure-algorithm-graph` | rewrite (147 w) | `Graph` |
| 24 | `data-structure-algorithm-breadth-first-search` | rewrite (**empty**) | `Graph` |
| 25 | `data-structure-algorithm-depth-first-search` | rewrite (**empty**) | `Graph` |

## Files

```
projects/java_datastructure/
  README.md            the requirements
  progress_report.md   this file
  manifest.py          category metadata + one entry per post
  posts/NN-slug.html   post bodies, plain semantic HTML
  src/dsa/*.java       the implementations — source of truth for every snippet
  tests/run.sh         javac -Werror + run all assertions
  seed.py              writes the posts into a content tree
  check_content.py     normaliser round-trip + snippets match src/
```

## Task log

| Date | Task | Owner | Status |
|---|---|---|---|
| 2026-08-18 | Audit the 24 live posts — words, empties, plaintext blocks | Claude | done |
| 2026-08-18 | Find the 4 inbound links from the LeetCode track | Claude | done |
| 2026-08-18 | Confirm Java 25 is installed and runs | Claude | done |
| 2026-08-18 | Agree Java version, scope, verification bar, publish path | Folau | done |
| 2026-08-18 | Write this progress report + the 25-post topic table | Claude | done |
| 2026-08-18 | Write 15 Java sources — 244 assertions, `-Werror` clean | Claude | done |
| 2026-08-18 | `manifest.py` / `seed.py` / `check_content.py` | Claude | done |
| 2026-08-18 | Author 25 post bodies — 21,900 words, 125 code blocks | Claude | done |
| 2026-08-18 | Add `JdkCollections.java` so the JDK snippets are verified too | Claude | done |
| 2026-08-18 | `check_content.py` — 339 Java lines matched to `src/dsa/` | Claude | done |
| 2026-08-18 | HTML well-formedness + internal-link check across all 25 | Claude | done |
| 2026-08-18 | Seed local `--force-dates --write` — 25 posts, category count 25 | Claude | done |
| 2026-08-18 | Build + `verify-build` — 549/549 posts, 44/44 counts agree | Claude | done |
| 2026-08-18 | Serve built output — all 25 URLs 200, reading order correct | Claude | done |
| 2026-08-18 | Folau authorised deploying without a pre-review | Folau | done |
| 2026-08-18 | Back up the prod tree — 679 objects, verified key+size | Claude | done |
| 2026-08-18 | Seed prod `--force-dates --write` — 575 posts, 25 in the category | Claude | done |
| 2026-08-18 | Build + deploy — 575/575, 1527 files, invalidated | Claude | done |
| 2026-08-18 | **Found the runner was silently using Java 21** — fixed, re-deployed | Claude | done |
| 2026-08-18 | Verify live — all 25 URLs 200, new content, correct order | Claude | done |
| | **Read the 25 published posts** | **Folau** | **next** |

## Publish state

| Tree | State |
|---|---|
| `local` | 25 posts, dates 2026-07-01 … 2026-08-18. 549 posts in the tree. |
| `prod` | **25 posts LIVE**, 575 posts total (was 574) |
| backup | `s3://lovemesomecoding-db-.../lovemesomecoding/backups/prod-2026-08-18-pre-data-structure/` |

Verified live after deploy: all 25 URLs return 200, the archive lists them in reading order, the
sitemap holds all 25, no page still carries the `boldgrid` / `wp-block-embed` markup, and the three
formerly empty slugs now serve 696–784 words with 219–306 Prism tokens each. `verify-build`
575/575 posts and 44/44 category counts agree.

Verified against the local tree: `verify-build` 549/549 posts, 44/44 category counts agree, 717
HTML files, all 25 URLs 200 off the built output, the archive lists them in reading order, and
Prism emits **5,684** highlighting tokens across the track (against 9 highlighted blocks before).

### Word counts — before and after

| | Before | After |
|---|---:|---:|
| Posts | 24 | **25** |
| Words | 16,756 | **21,900** |
| Code blocks | 50 | **125** |
| Highlighted blocks | 9 | **124** |
| Posts with `<h2>` | 3 | **25** |
| Empty posts | 3 | **0** |

The three empty slugs — `merge-sort`, `breadth-first-search`, `depth-first-search` — now run 1,100,
924 and 921 words with working, asserted code.

### ⚠️ Before seeding prod

**S3 object versioning is still not enabled on the content bucket** — confirmed during the
`/spring-study-guide` publish. Overwriting a post is irreversible and this publish rewrites 24
indexed URLs, so copy the prod tree to `backups/prod-<date>-pre-data-structure/` first and verify
it on key *and* size, not just object count.

## ⚠️ The bug the deploy caught — the runner was on the wrong JDK

Found while verifying the live pages, not before: the get-started post's sample output still read
`244 passed` and omitted `JdkCollections`. Regenerating it from an actual run surfaced the real
problem — the first line said **`Java 21`**.

`tests/run.sh` honoured an existing `JAVA_HOME`, and on this machine that variable points at
Corretto 21. So the suite had been running green on Java 21 while the whole track claims Java 25.
Nothing failed; it simply was not testing what it said it was.

Two fixes:

1. **`tests/run.sh` now requires Java 25 and fails loudly below it**, ignoring `JAVA_HOME`
   (override with `DSA_JAVA_HOME`). A silent fallback to an older toolchain is exactly the failure
   mode this track spends 25 posts warning about, so it is an error rather than a shrug.
2. **The sample output is regenerated from a real run** instead of being typed by hand — which is
   how it went stale in the first place.

Worth noting the code is genuinely fine on both: it compiles and passes all 261 assertions under
Java 21 and Java 25 alike. The defect was the claim, not the code.

## One design change made while writing

The priority-queue post was mostly `PriorityQueue` usage, and the stack, queue and binary-search
posts each ended with "here is the JDK class you would actually use". Those snippets were the ones
a reader is *most* likely to copy — and they were the only Java on the site that nothing compiled,
which put a hole in the track's whole premise exactly where it mattered most.

`src/dsa/JdkCollections.java` fixes that: the standard-library examples are now real, compiled,
asserted code (261 assertions, up from 244). Several assertions pin behaviour that surprises
people — that a `PriorityQueue` does not iterate in sorted order, that `ArrayDeque.push` adds to the
front, and what `Arrays.binarySearch` returns on a miss.

`check_content.py` also reports what it could *not* verify rather than staying silent: 10
illustrative lines in the two conceptual posts (`memory`, `big-o-notation`). Anything else needs an
explicit `illustrative` entry in the manifest, and a stale entry is itself a failure — so the
exception cannot quietly widen.

## Outstanding

1. **Backend Lambda still not redeployed** — inherited from the React, Spring Boot and Spring Study
   Guide tracks. Seeding runs the local service layer so what lands in S3 is correct, but editing
   these posts through `/admin` before `lovemesomecoding_backend/scripts/deploy.sh` runs would
   normalise unknown languages down to `plaintext`. Now affects four tracks.
2. **Enable S3 object versioning** on the content bucket. Four tracks have each needed a manual
   backup step that one bucket setting would make unnecessary.
3. **`deploy.sh` cannot verify a content-only deploy.** Documented in
   `projects/leetcode/progress_report.md`: the build id comes from `git rev-parse HEAD` in the
   *frontend* repo, so a content-only publish never changes it and the final check compares a value
   to itself. Verify by fetching the new URLs instead — as the last three tracks did.
