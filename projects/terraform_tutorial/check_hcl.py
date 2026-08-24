#!/usr/bin/env python3
"""Prove every HCL block in the track is real Terraform, offline.

This is the Terraform analogue of the AWS track's check_aws.py, and it targets
exactly how old infrastructure content rots: an argument gets renamed, a resource
moves to a different provider, a block type is removed — and the sample still
LOOKS perfect. Nothing about reading it tells you it stopped working two provider
majors ago.

`terraform validate` decides, against the real downloaded provider schema, so for
every block we prove:

    the resource type exists       aws_ecs_service       -> yes
    the argument exists on it      health_check_grace…   -> yes
    the block type is allowed      runtime_platform      -> yes

offline, in milliseconds each, with no credentials and nothing billed.

    python projects/terraform_tutorial/check_hcl.py
    python projects/terraform_tutorial/check_hcl.py --post terraform-with-aws -v
    python projects/terraform_tutorial/check_hcl.py --infra      # the applied stack

WHAT IT DOES NOT PROVE, stated plainly so nobody trusts it further than it goes:

  - Not that `apply` succeeds. No account, permission, quota or resource state is
    consulted. This is a type check, not a deployment.
  - Not that argument VALUES are valid. `instance_class = "banana"` passes;
    `instance_clas` fails.
  - Not that the resulting infrastructure is correct, reachable or secure.

A post block is usually a FRAGMENT — a few lines of one resource, quoted to make
a point, referring to resources defined in another block or another lesson. Those
cannot validate as written, so this script distinguishes:

  ok        validated clean
  fragment  only failed on references to things not in the block (an expected
            shape for tutorial prose) — reported, does not fail the run
  FAIL      the provider rejected something it was asked about: an unknown
            argument, an unknown resource type, a removed block. This is rot.

To make fragments validate more often, undeclared `var.x` and `local.x`
references are synthesised before validating, so a block that is honest apart
from its inputs comes out `ok` rather than `fragment`.
"""

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
INFRA = HERE / "infra"

sys.path.insert(0, str(HERE))
import manifest  # noqa: E402

# Prism language classes that hold Terraform. `terraform` is the Prism alias;
# `hcl` is the older one. Both render, so both are accepted here.
HCL_LANGS = {"hcl", "terraform"}

CODE_BLOCK = re.compile(
    r'<pre class="language-([\w-]+)"><code class="language-[\w-]+">(.*?)</code></pre>', re.S)

# Errors that mean the provider rejected something it genuinely knows about.
# These are the ones worth failing a build over — they are what "this tutorial is
# out of date" actually looks like in a diagnostic.
ROT_SUMMARIES = (
    "Unsupported argument",
    "Unsupported block type",
    "Invalid resource type",
    "Invalid data source",
    "Unsupported meta-argument",
    "Invalid block definition",
    "Argument or block definition required",
    "Missing required argument",
    "Invalid expression",
    "Unbalanced braces",
    "Invalid function name",
    "Call to unknown function",
)

# Errors that only mean "this block quotes something defined elsewhere", which is
# the normal shape of a tutorial snippet.
FRAGMENT_SUMMARIES = (
    "Reference to undeclared resource",
    "Reference to undeclared module",
    "Reference to undeclared input variable",
    "Reference to undeclared local value",
    "Invalid reference",
    "Cycle",
    # A `module` block whose source directory is not present in the throwaway
    # workspace. Lesson 10 is entirely module calls, and the modules they name
    # live in infra/ — quoting the call without shipping the callee is the normal
    # shape, not rot. `terraform validate` cannot see past an uninstalled module,
    # so the arguments inside these blocks are NOT schema-checked; that is a real
    # limit of this checker and is stated in the README.
    "Module not installed",
    "Unreadable module directory",
    "Module not found",
    "Module source not found",
)

VAR_REF = re.compile(r'\bvar\.([a-zA-Z_][a-zA-Z0-9_-]*)')
LOCAL_REF = re.compile(r'\blocal\.([a-zA-Z_][a-zA-Z0-9_-]*)')
DECLARED_VAR = re.compile(r'^\s*variable\s+"([^"]+)"', re.M)
DECLARED_LOCALS = re.compile(r'^\s*locals\s*\{', re.M)

# A block that declares its own terraform{} settings must not get ours as well.
HAS_TERRAFORM_BLOCK = re.compile(r'^\s*terraform\s*\{', re.M)
HAS_PROVIDER_BLOCK = re.compile(r'^\s*provider\s+"aws"', re.M)

# .terraform.lock.hcl is HCL, and it is worth quoting — lesson 4 is largely about
# it — but it is NOT a Terraform configuration. `validate` rejects it with
# "invalid provider local name: dots are not allowed", because it reads the
# registry address as a local name.
#
# Detected by shape rather than by a marker comment in the post, so that readers
# see a clean lock file rather than an annotation aimed at this script.
LOCKFILE_BLOCK = re.compile(
    r'^\s*provider\s+"registry\.terraform\.io/[^"]+"\s*\{', re.M)

VERSIONS_TF = '''terraform {
  required_version = ">= 1.10"
  required_providers {
    aws    = { source = "hashicorp/aws", version = "~> 6.0" }
    random = { source = "hashicorp/random", version = "~> 3.6" }
  }
}

provider "aws" {
  region                      = "us-west-2"
  # No credentials are used or needed: validate never contacts AWS. These stop
  # the provider complaining about an unconfigured region on a machine that has
  # no AWS environment at all, which is the point — this must run in CI.
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true
  access_key                  = "mock"
  secret_key                  = "mock"
}
'''


def terraform_bin() -> str:
    exe = shutil.which("terraform")
    if not exe:
        raise SystemExit(
            "terraform is not on PATH.\n"
            "This track is written against 1.15.9. Note that `brew upgrade terraform` "
            "fails on this machine with an unrelated Xcode error — see progress_report.md; "
            "the binary was installed from HashiCorp's release into ~/bin."
        )
    return exe


def make_workspace(tf: str) -> Path:
    """One initialised workspace, reused for every block.

    `terraform init` downloads ~700 MB of provider on a cold cache and takes
    tens of seconds. Doing it once and rewriting a single .tf file between
    validations turns a 4-minute run into a 4-second one.
    """
    ws = Path(tempfile.mkdtemp(prefix="tfcheck-"))
    (ws / "versions.tf").write_text(VERSIONS_TF)

    # Reuse the providers already downloaded for infra/, when they are there.
    local_plugins = INFRA / ".terraform" / "providers"
    env = dict(os.environ)
    if local_plugins.is_dir():
        env["TF_PLUGIN_CACHE_DIR"] = str(local_plugins.parent / "plugin-cache")
        Path(env["TF_PLUGIN_CACHE_DIR"]).mkdir(parents=True, exist_ok=True)

    proc = subprocess.run(
        [tf, "init", "-backend=false", "-input=false", "-no-color"],
        cwd=ws, capture_output=True, text=True, env=env,
    )
    if proc.returncode != 0:
        shutil.rmtree(ws, ignore_errors=True)
        raise SystemExit(f"could not initialise a validation workspace:\n{proc.stdout}\n{proc.stderr}")
    return ws


def synthesise_inputs(body: str) -> str:
    """Declare the var./local. references the block does not declare itself.

    A snippet that says `var.name_prefix` is not wrong — it is quoted out of a
    module that declares it. Synthesising the declaration lets the block be
    judged on the part that matters: whether the provider accepts its arguments.
    """
    extra = []

    declared = set(DECLARED_VAR.findall(body))
    referenced = set(VAR_REF.findall(body))
    for name in sorted(referenced - declared):
        # No type constraint: `any` accepts whatever the block does with it.
        extra.append(f'variable "{name}" {{\n  default = "check_hcl_placeholder"\n}}')

    locals_referenced = sorted(set(LOCAL_REF.findall(body)))
    if locals_referenced and not DECLARED_LOCALS.search(body):
        pairs = "\n".join(f'  {n} = "check_hcl_placeholder"' for n in locals_referenced)
        extra.append(f"locals {{\n{pairs}\n}}")

    return "\n\n".join(extra)


def is_deprecation(d: dict) -> bool:
    """A warning that says a block or argument is on its way out.

    ⚠️ These are ERRORS for this track's purposes, even though Terraform calls
    them warnings.

    Deprecation is what rot looks like BEFORE it breaks, and it is exactly the
    trap this track exists to avoid walking readers into. The canonical example
    is the AWS provider's S3 split:

        resource "aws_s3_bucket" "this" {
          versioning { enabled = true }     # valid, and deprecated since v4
        }

    `terraform validate` returns valid:true with one warning. Every pre-2022
    tutorial on the internet still shows it. Shipping it in something written in
    2026 would put this track in the same category, so a deprecation fails the
    check and has to be written the current way.
    """
    text = f"{d.get('summary', '')} {d.get('detail', '')}".lower()
    return "deprecat" in text


def classify(diagnostics: list) -> tuple:
    """Split diagnostics into the ones that mean rot and the ones that mean fragment."""
    rot, fragment, other = [], [], []
    for d in diagnostics:
        severity = d.get("severity")
        if severity == "warning":
            if is_deprecation(d):
                rot.append(d)
            continue
        if severity != "error":
            continue
        summary = d.get("summary", "")
        if any(summary.startswith(s) for s in ROT_SUMMARIES):
            rot.append(d)
        elif any(summary.startswith(s) for s in FRAGMENT_SUMMARIES):
            fragment.append(d)
        else:
            other.append(d)
    return rot, fragment, other


def validate_block(tf: str, ws: Path, body: str) -> tuple:
    """Validate one block. Returns (status, diagnostics)."""
    # A lock file is HCL but not a configuration; validate cannot judge it and
    # its complaint would be about provider naming rather than about anything
    # the post got wrong.
    if LOCKFILE_BLOCK.search(body):
        return "lockfile", []

    for stale in ws.glob("block*.tf"):
        stale.unlink()

    # A block that brings its own terraform{}/provider blocks would collide with
    # the workspace's. Drop ours for the duration.
    versions = ws / "versions.tf"
    restore = None
    if HAS_TERRAFORM_BLOCK.search(body) or HAS_PROVIDER_BLOCK.search(body):
        restore = versions.read_text()
        # Keep the provider config unless the block supplies its own, or the
        # provider complains about a missing region on a bare machine.
        if HAS_PROVIDER_BLOCK.search(body):
            versions.write_text("")
        else:
            versions.write_text(VERSIONS_TF.split("terraform {", 1)[0] +
                                VERSIONS_TF[VERSIONS_TF.index("provider \"aws\""):])

    (ws / "block.tf").write_text(body)
    synth = synthesise_inputs(body)
    if synth:
        (ws / "block_inputs.tf").write_text(synth)

    proc = subprocess.run(
        [tf, "validate", "-json", "-no-color"],
        cwd=ws, capture_output=True, text=True,
    )

    if restore is not None:
        versions.write_text(restore)

    try:
        result = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return "FAIL", [{"summary": "terraform validate produced no JSON",
                         "detail": (proc.stderr or proc.stdout)[:400]}]

    # ⚠️ Do NOT short-circuit on result["valid"].
    #
    # A deprecation comes back as valid:true with a warning attached, so an early
    # return here would pass exactly the blocks this script is most meant to
    # catch — syntax that still works and should no longer be taught.
    rot, fragment, other = classify(result.get("diagnostics", []))
    if result.get("valid") and not rot:
        return "ok", []
    if rot or other:
        return "FAIL", rot + other
    if fragment:
        return "fragment", fragment
    return "ok", []


def blocks_in(path: Path) -> list:
    """Every HCL code block in a post, unescaped back to its authored source."""
    raw = path.read_text(encoding="utf-8")
    out = []
    for lang, body in CODE_BLOCK.findall(raw):
        if lang in HCL_LANGS:
            out.append(html.unescape(body))
    return out


def check_infra(tf: str) -> int:
    """Validate the applied stack itself — root module and every child module."""
    print("infra/ — the stack that was applied to AWS\n")
    failures = 0
    targets = [INFRA] + sorted(p for p in (INFRA / "modules").glob("*") if p.is_dir())

    # ⚠️ A shared plugin cache, or this function leaves 1.6 GB behind PER
    # DIRECTORY. `terraform init` downloads the provider into ./.terraform by
    # default, and there are four directories here — the first version of this
    # put 3.9 GB in projects/terraform_tutorial. With the cache set, the four
    # initialisations share one copy and link to it.
    env = dict(os.environ)
    cache = Path(tempfile.gettempdir()) / "tfcheck-plugin-cache"
    cache.mkdir(parents=True, exist_ok=True)
    env["TF_PLUGIN_CACHE_DIR"] = str(cache)

    for target in targets:
        if not any(target.glob("*.tf")):
            continue
        rel = target.relative_to(REPO_ROOT)
        init = subprocess.run(
            [tf, "init", "-backend=false", "-input=false", "-no-color"],
            cwd=target, capture_output=True, text=True, env=env)
        if init.returncode != 0:
            print(f"  FAIL  {rel}  (init)\n{init.stderr[:400]}")
            failures += 1
            continue
        # -json, and the diagnostics inspected, for the same reason the post
        # checker does it: a DEPRECATION is a warning, so plain `validate` exits
        # 0 on it. The stack the AWS lessons quote must not be teaching syntax
        # that is already on its way out.
        val = subprocess.run([tf, "validate", "-json", "-no-color"],
                             cwd=target, capture_output=True, text=True)
        fmt = subprocess.run([tf, "fmt", "-check", "-recursive", "-no-color", "."],
                             cwd=target, capture_output=True, text=True)

        deprecations = []
        val_ok = val.returncode == 0
        try:
            parsed = json.loads(val.stdout)
            deprecations = [d for d in parsed.get("diagnostics", []) if is_deprecation(d)]
            val_ok = parsed.get("valid", False) and not deprecations
        except json.JSONDecodeError:
            val_ok = False

        # Drop the per-directory .terraform as soon as this target is judged.
        # Even linked against the shared cache it is clutter inside the repo, and
        # the child modules are never initialised in ordinary use — only here.
        shutil.rmtree(target / ".terraform", ignore_errors=True)
        if target != INFRA:
            (target / ".terraform.lock.hcl").unlink(missing_ok=True)

        ok = val_ok and fmt.returncode == 0
        print(f"  {'ok  ' if ok else 'FAIL'}  {rel}"
              f"{'' if val_ok else '  (validate)'}"
              f"{'' if fmt.returncode == 0 else '  (fmt)'}")
        if not ok:
            failures += 1
            for d in deprecations:
                print(f"      deprecated: {d.get('summary')} — {(d.get('detail') or '')[:120]}")
            if not deprecations:
                print((val.stdout or val.stderr)[:600])
            if fmt.stdout:
                print(f"    unformatted: {fmt.stdout.strip()}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--post", default=None, help="check one slug")
    parser.add_argument("--infra", action="store_true",
                        help="check infra/ instead of the posts")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print the diagnostics for fragments too")
    args = parser.parse_args()

    tf = terraform_bin()
    version = subprocess.run([tf, "version", "-json"], capture_output=True, text=True)
    try:
        tf_version = json.loads(version.stdout)["terraform_version"]
    except Exception:
        tf_version = "unknown"
    print(f"terraform {tf_version}  ({tf})\n")

    if args.infra:
        failures = check_infra(tf)
        print()
        if failures:
            print(f"FAILED: {failures} director{'y' if failures == 1 else 'ies'}")
            return 1
        print("infra/ validates and is formatted")
        return 0

    entries = manifest.POSTS
    if args.post:
        entries = [e for e in entries if e["slug"] == args.post]
        if not entries:
            raise SystemExit(f"not in the manifest: {args.post}")

    ws = make_workspace(tf)
    try:
        total = ok = frag = lockfiles = 0
        failures = []
        written = 0

        for entry in entries:
            path = HERE / "posts" / entry["file"]
            if not path.exists():
                print(f"{entry['slug']:44} not written")
                continue
            written += 1
            blocks = blocks_in(path)
            if not blocks:
                print(f"{entry['slug']:44} no HCL blocks")
                continue

            statuses = []
            for i, body in enumerate(blocks):
                status, diags = validate_block(tf, ws, body)
                total += 1
                statuses.append(status)
                if status == "ok":
                    ok += 1
                elif status == "lockfile":
                    lockfiles += 1
                elif status == "fragment":
                    frag += 1
                    if args.verbose:
                        for d in diags:
                            print(f"    fragment {entry['slug']} block {i}: {d.get('summary')}")
                else:
                    failures.append((entry["slug"], i, diags, body))

            counts = {s: statuses.count(s) for s in set(statuses)}
            summary = "  ".join(f"{v} {k}" for k, v in sorted(counts.items()))
            print(f"{entry['slug']:44} {len(blocks):>2} HCL blocks   {summary}")

        print(f"\n{written} post(s) written, {total} HCL blocks: "
              f"{ok} validated, {frag} fragment, "
              f"{lockfiles} lock file, {len(failures)} failed")

        if failures:
            print("\nFAILED — the provider rejected these:\n")
            for slug, i, diags, body in failures:
                print(f"  x {slug} block {i}")
                for d in diags:
                    where = d.get("range", {}).get("start", {}).get("line")
                    print(f"      {d.get('summary')}"
                          f"{f' (line {where})' if where else ''}")
                    if d.get("detail"):
                        print(f"        {d['detail'][:200]}")
                first = body.strip().splitlines()[:3]
                for line in first:
                    print(f"      | {line}")
                print()
            return 1

        if total == 0:
            print("nothing to check yet")
            return 0
        print("every HCL block is real Terraform against the pinned provider")
        return 0
    finally:
        shutil.rmtree(ws, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
