# RAG tutorial: progress report

**Status (2026-11-14): lesson 2 code written; retrieval verified, generation untested** (no Anthropic
API key on this machine yet). Setup committed in the code repo (`88c186e`); lesson 2 uncommitted.

## Lesson 2 findings (naive RAG, `lessons/02_naive_rag.py`) — material for later lessons
8,171 fixed 1,000-char chunks, embedded in ~35 s on Apple Silicon (MPS), cached in `data/naive_index.npz`.
- **"What is a Python decorator?" → #1 is `/typescript/typescript-decorators`**; the Python post is #3.
  Chunks don't carry the post title, so the language is lost. Fix: title/metadata in chunks (L3),
  contextual retrieval (L8).
- **Code is mangled**: stripping Prism `<span>`s leaves `System . out . println ( ...`. Fix: L3.
- **`Copy` button text** leaks into every code chunk. Fix: L3.
- **Chunks start mid-word** (`t i = 0 ; i < 1_000_000`). Fix: L3 (split on structure).
- **Duplicate sources**: 3 of top 5 for "create a thread in Java" are the same post. Fix: L6 (dedupe/rerank).
- "CORS in Spring Boot" retrieves sensibly (0.83) — naive is not useless, which is the point of L1.

## Setup notes (2026-11-14)
- **Export reads the public site, not S3**: `search-index.json` (989 entries) + each post page's
  `<article class="prose">`. Readers can run it without AWS access. (The README's original plan said
  `prod/posts/` from S3; changed because readers have no access to that bucket.)
- Exported HTML is the **rendered** page: code is already escaped and Prism-highlighted (`<span>`s
  inside `<pre>`), and each block has a `Copy` button whose text leaks into `get_text()`. The
  raw-`<script>`-in-code gotcha from the WordPress migration does not apply here; stripping
  highlight spans and copy buttons does. 8,088 `<pre>` blocks in total.
- **18 posts are near-empty stubs on the live site** (e.g. `/css/css-grid` is just "Source code on
  Github", several `spring-interview/*` are empty). Real content, not an export bug — use them in the
  chunking lesson as "filter junk before indexing".
- Port **5434** (5432 = local Postgres, 5433 = another container on this machine).
- Python.org macOS Python has no root certs, so `urllib` fails with CERTIFICATE_VERIFY_FAILED. The
  script uses `requests` (certifi) instead.

## Decisions (2026-11-14)
| Question | Decision |
|---|---|
| Project | "Ask LoveMeSomeCoding": Q&A with citations over the site's own posts |
| Data | lovemesomecoding.com posts only (one-time read-only export of `prod/posts/`). Pizza app dropped |
| Infrastructure | All local, tutorial use only. No AWS deploy, no live widget |
| Vector DB | Postgres + pgvector (Docker). Keyword side of hybrid search = Postgres full-text search |
| Graph DB | Not needed — dropped |
| Embeddings | Local (sentence-transformers); local cross-encoder reranker |
| LLM | Claude API (only external dependency) |
| Language | Python |
| Code repo | `ai_repo_lovemesomecoding.com` (public, `folaulau/`), nested at parent root, gitignored by parent |
| Category / nav | `rag`, in the existing **AI** nav group |
| Embedding model | `BAAI/bge-small-en-v1.5` (384-dim); lesson 4 compares one alternative |

## Open questions
- None.

## Proposed outline
| # | Topic | Status |
|---|---|---|
| 1 | What RAG is, and when you don't need it (long context, plain search) | planned |
| 2 | Naive RAG in ~50 lines: embed, cosine similarity, prompt | code written, generation untested |
| 3 | Chunking: by heading, keep code blocks whole, metadata (the `<pre>` gotcha) | planned |
| 4 | Embeddings + pgvector: schema, indexing, similarity queries | planned |
| 5 | A golden question set: measuring retrieval (recall@k, MRR) | planned |
| 6 | Hybrid search (full-text + vector) and reranking | planned |
| 7 | Citations, and making the model say "I don't know" | planned |
| 8 | Contextual retrieval: prefixing chunks with post context | planned |
| 9 | Evaluating answers: groundedness and correctness | planned |
| 10 | Re-indexing when content changes | planned |
| 11 | Capstone: RAG + tools — retrieval for content, structured queries for "latest posts in X" | planned |

## Owners
- Folau: decisions, review, publishing.
- Claude: code in `ai_repo_lovemesomecoding.com`, lesson drafts, golden set, measurements.
