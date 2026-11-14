# RAG Tutorial

## About
- A tutorial series that teaches **Retrieval-Augmented Generation by building one real thing**:
  "Ask LoveMeSomeCoding", a question-answering assistant over the site's own ~977 posts that answers
  from the tutorials and cites the posts it used.
- Audience: aspiring and working developers who can write Python but have never built RAG.
- Every lesson changes the same project and **measures** the change. Retrieval quality is shown with
  numbers from a golden question set, not asserted.

## Requirements (agreed 2026-11-14)
- **Data = lovemesomecoding.com posts**, exported from the public site (`search-index.json` + each
  post page) by `scripts/export_posts.py` into `data/` (gitignored). No AWS access needed.
- **Everything runs locally.** Tutorial use only: no Lambda, no S3 Vectors, no live widget on the site.
  The only network dependency is the Claude API call for answer generation.
- **Vector DB: Postgres + pgvector in Docker.** One container. Keyword search for hybrid retrieval uses
  Postgres full-text search, so no Elasticsearch. **No graph DB** — RAG does not need one.
- **Embeddings: local** (sentence-transformers), free and offline. Reranker also local (cross-encoder).
- **Python.**
- **Code lives in `ai_repo_lovemesomecoding.com`** (nested at the parent repo root, gitignored there;
  **public** GitHub repo `folaulau/ai_repo_lovemesomecoding.com`). Exported post data stays out of it:
  readers run the export script themselves.
- **Category `rag`**, appended to the existing **AI** nav group in
  `lovemesomecoding_frontend/src/lib/nav.ts`.
- **Embedding model `BAAI/bge-small-en-v1.5`** (384-dim). Lesson 4 compares one alternative with real
  numbers.

## Layout
Code: `../../ai_repo_lovemesomecoding.com/` (docker-compose.yml, Python package, `data/` gitignored).
Docs and posts:
```
projects/rag_tutorial/
  README.md            this file
  progress_report.md   status, decisions, lesson table (read first)
  posts/NN-slug.html   post bodies (same conventions as other tracks)
  manifest.py          category metadata + one entry per post
  seed.py / check_content.py   same role as in projects/ai_engineering
```

## Content gotcha that becomes a lesson
Post bodies contain raw `<script>`, `<button onclick>` and `<style>` *inside* code samples. Extract
`<pre>` blocks with regex **before** any HTML parsing, or `get_text()` silently deletes code. The
chunking lesson teaches this directly.
