#!/usr/bin/env python3
"""Snapshot the prose of the 33 live AWS posts, so check_content.py can prove a rewrite happened.

The interesting defect in this track is not "the post is short". It is "the post is copied AWS
marketing blurb", and the way that survives a rewrite is by being pasted back in. Catching that
needs the ORIGINAL text to compare against, so it is captured here rather than read from a synced
content tree at check time — a check that depends on someone having run sync-content is a check
that silently skips.

⚠️ RUN THIS ONCE, BEFORE THE REWRITES ARE PUBLISHED. It is now too late to re-take it.

The snapshot is the "before". Once the rewrites are live in the prod tree — which they are — this
script would read the NEW bodies and store them as the originals. Rule 4b would then compare every
post against itself, find a 100% overlap, and fail the whole track; or worse, be "fixed" by
lowering the threshold, at which point the check is measuring nothing.

So it refuses to overwrite an existing snapshot. `--force` exists for the one legitimate case:
starting a fresh track whose originals have genuinely not been touched yet.

    AWS_PROFILE=folau lovemesomecoding_backend/.venv/bin/python \
        projects/aws_tutorial/originals/snapshot.py
"""
import gzip, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE.parent))
os.environ.setdefault("env", "test")
os.environ.setdefault("data_env", "test")

import manifest  # noqa: E402

TREE = ROOT / "lovemesomecoding_frontend/content/posts"
if not TREE.exists():
    raise SystemExit(f"no content tree at {TREE}. Run lovemesomecoding_frontend/scripts/sync-content.sh")

TAGS = re.compile(r"<[^>]+>")
PRE = re.compile(r"<pre.*?</pre>", re.S | re.I)


def prose(html: str) -> str:
    """Rendered prose only — code blocks removed, entities and whitespace normalised."""
    import html as h
    text = PRE.sub(" ", html)
    text = TAGS.sub(" ", text)
    text = h.unescape(text).replace("\xa0", " ")
    return " ".join(text.split())


out = {}
for entry in manifest.POSTS:
    # A NEW post has no "before" to snapshot — there is no live body it replaces. It is still
    # checked against every other post's original by rule 4b, so nothing is skipped there.
    if entry["slug"] in manifest.NEW_SLUGS:
        continue
    path = TREE / f"{entry['slug']}.json"
    if not path.exists():
        raise SystemExit(f"{entry['slug']} is not in the content tree — is it synced to prod?")
    out[entry["slug"]] = prose(json.loads(path.read_text())["contentHtml"])

dest = HERE / "prose.json.gz"
if dest.exists() and "--force" not in sys.argv:
    raise SystemExit(
        f"{dest.name} already exists — refusing to overwrite.\n\n"
        "This file is the PRE-REWRITE text of the live posts, and the rewrites are already "
        "published. Re-taking it now would capture the new bodies as the originals, which makes "
        "rule 4b compare every post against itself.\n\n"
        "If you genuinely mean to re-baseline, pass --force.")

with gzip.open(dest, "wt", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=0, sort_keys=True)

words = sum(len(v.split()) for v in out.values())
print(f"wrote {dest.relative_to(ROOT)}  —  {len(out)} posts, {words:,} prose words, "
      f"{dest.stat().st_size:,} bytes gzipped")
