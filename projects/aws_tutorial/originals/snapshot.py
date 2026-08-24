#!/usr/bin/env python3
"""Snapshot the prose of the 33 live AWS posts, so check_content.py can prove a rewrite happened.

The interesting defect in this track is not "the post is short". It is "the post is copied AWS
marketing blurb", and the way that survives a rewrite is by being pasted back in. Catching that
needs the ORIGINAL text to compare against, so it is captured here rather than read from a synced
content tree at check time — a check that depends on someone having run sync-content is a check
that silently skips.

Run once (or after the live posts change, which they should not):

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
    path = TREE / f"{entry['slug']}.json"
    if not path.exists():
        raise SystemExit(f"{entry['slug']} is not in the content tree — is it synced to prod?")
    out[entry["slug"]] = prose(json.loads(path.read_text())["contentHtml"])

dest = HERE / "prose.json.gz"
with gzip.open(dest, "wt", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=0, sort_keys=True)

words = sum(len(v.split()) for v in out.values())
print(f"wrote {dest.relative_to(ROOT)}  —  {len(out)} posts, {words:,} prose words, "
      f"{dest.stat().st_size:,} bytes gzipped")
