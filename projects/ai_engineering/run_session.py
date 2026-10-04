#!/usr/bin/env python3
"""Run one real Claude Code session against the pizza app and keep the transcript.

The posts in this track quote prompts and output, and the rule is that every quote comes from a
session that actually ran. This runs `claude -p` headless in the demo app, records the raw
stream-json and writes a readable transcript next to it:

    python projects/ai_engineering/run_session.py 04-analysis --mode plan --prompt-file p.txt
    python projects/ai_engineering/run_session.py 07-code --resume <session-id> --prompt "..."

    sessions/<name>.jsonl   raw event stream (source of truth)
    sessions/<name>.md      prompt, every tool call, and the final answer, for quoting

`--mode plan` keeps the session read-only. The session id is printed so a later step can resume
the same conversation, which is how the series follows one feature through several posts.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parent.parent / "lovemesomecoding_demo_project" / "pizza"
OUT = HERE / "sessions"


def summarise_input(name: str, data: dict) -> str:
    for key in ("command", "file_path", "pattern", "path", "url", "description"):
        if key in data:
            return f"{key}={str(data[key])[:200]!r}"
    return json.dumps(data)[:200]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--mode", default="plan",
                        choices=("plan", "acceptEdits", "default", "bypassPermissions"))
    parser.add_argument("--resume")
    parser.add_argument("--cwd", default=str(APP))
    parser.add_argument("--allow", nargs="*", default=[],
                        help='extra tools to pre-approve, e.g. "Bash(./mvnw:*)"')
    args = parser.parse_args()

    prompt = args.prompt or Path(args.prompt_file).read_text(encoding="utf-8")
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--permission-mode", args.mode]
    if args.resume:
        cmd += ["--resume", args.resume]
    if args.allow:
        cmd += ["--allowedTools", *args.allow]

    OUT.mkdir(exist_ok=True)
    raw_path = OUT / f"{args.name}.jsonl"
    md = [f"# Session {args.name}\n", f"mode: `{args.mode}`  cwd: `{args.cwd}`"
          + (f"  allowed: `{' '.join(args.allow)}`" if args.allow else "")
          + (f"  resumed: `{args.resume}`" if args.resume else "") + "\n",
          "## Prompt\n", "```text", prompt.strip(), "```\n", "## Transcript\n"]
    session_id, final, cost = None, "", None

    with raw_path.open("w", encoding="utf-8") as raw:
        proc = subprocess.Popen(cmd, cwd=args.cwd, stdout=subprocess.PIPE, text=True)
        for line in proc.stdout:
            raw.write(line)
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            session_id = event.get("session_id", session_id)
            if event.get("type") == "assistant":
                for part in event["message"].get("content", []):
                    if part.get("type") == "text" and part["text"].strip():
                        md += [part["text"].strip(), ""]
                    elif part.get("type") == "tool_use":
                        md.append(f"- **{part['name']}** {summarise_input(part['name'], part['input'])}")
            elif event.get("type") == "result":
                final = event.get("result", "")
                cost = event.get("total_cost_usd")
                md += ["", f"_turns: {event.get('num_turns')}, "
                           f"duration: {event.get('duration_ms', 0) / 1000:.0f}s, "
                           f"cost: ${cost or 0:.2f}_"]
        proc.wait()

    md += ["\n## Final answer\n", final]
    (OUT / f"{args.name}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"session_id {session_id}\ntranscript {OUT / (args.name + '.md')}")
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
