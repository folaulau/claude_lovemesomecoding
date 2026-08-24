#!/usr/bin/env python3
"""Prove check_hcl.py actually catches things.

A checker that passes everything is worse than no checker, because it is
believed. This plants each class of error the script exists to catch and asserts
it is reported — and asserts that honest fragments are NOT reported, which is the
half that makes the tool usable.

    python3 projects/terraform_tutorial/tests/test_check_hcl.py

No AWS credentials. It does need `terraform` on PATH and one provider download
(cached after the first run).
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRACK = HERE.parent
sys.path.insert(0, str(TRACK))

import check_hcl  # noqa: E402

GOOD = '''resource "aws_ecs_cluster" "this" {
  name = "pizza-tf"

  tags = {
    Project = "terraform-tutorial"
  }
}'''

# Each of these is a real way infrastructure content goes stale.
ROT_CASES = [
    (
        "argument renamed or removed",
        '''resource "aws_ecs_cluster" "this" {
  namez = "pizza-tf"
}''',
    ),
    (
        "resource type that does not exist",
        '''resource "aws_ecs_klaster" "this" {
  name = "pizza-tf"
}''',
    ),
    (
        "nested block not allowed here",
        '''resource "aws_ecs_cluster" "this" {
  name = "pizza-tf"
  not_a_block { x = 1 }
}''',
    ),
    (
        "deprecated argument (a WARNING to terraform, rot to us)",
        # The classic AWS provider S3 split. `terraform validate` returns
        # valid:true with a deprecation warning, so this passes an ordinary
        # validate and is exactly what every pre-2022 tutorial still shows.
        '''resource "aws_s3_bucket" "this" {
  bucket = "example"
  versioning {
    enabled = true
  }
}''',
    ),
    (
        "function that does not exist",
        '''locals {
  x = definitely_not_a_function("a")
}''',
    ),
]

# These are honest snippets that reference things defined elsewhere. They must be
# reported as `fragment`, never as failures — otherwise every quoted excerpt in
# the track would fail the build and the checker would be turned off.
FRAGMENT_CASES = [
    (
        "references a resource defined in another block",
        '''resource "aws_ecs_service" "this" {
  name    = "pizza-tf"
  cluster = aws_ecs_cluster.elsewhere.id
}''',
    ),
    (
        "a module block whose source lives elsewhere",
        '''module "network" {
  source = "./modules/network"

  name_prefix = "pizza-tf"
}''',
    ),
    (
        "references a module output from another lesson",
        '''resource "aws_db_subnet_group" "this" {
  name       = "pizza-tf-db"
  subnet_ids = module.network.private_subnet_ids
}''',
    ),
]

# A snippet using undeclared var./local. should be SYNTHESISED into validity, so
# it comes out ok rather than fragment. This is what keeps most real snippets in
# the strict lane.
SYNTHESISED_CASES = [
    (
        "undeclared var. references are synthesised",
        '''resource "aws_ecs_cluster" "this" {
  name = var.name_prefix
  tags = var.tags
}''',
    ),
    (
        "undeclared local. references are synthesised",
        '''resource "aws_ecs_cluster" "this" {
  name = local.cluster_name
}''',
    ),
]


def main() -> int:
    tf = check_hcl.terraform_bin()
    ws = check_hcl.make_workspace(tf)
    failures = []

    try:
        # The control. If this does not pass, every other result is meaningless.
        status, diags = check_hcl.validate_block(tf, ws, GOOD)
        if status != "ok":
            failures.append(f"the known-good block did not validate: {status} "
                            f"{[d.get('summary') for d in diags]}")
            print(f"  FAIL  control block -> {status}")
        else:
            print("  ok    control block validates")

        print("\n  rot — must FAIL:")
        for label, body in ROT_CASES:
            status, diags = check_hcl.validate_block(tf, ws, body)
            ok = status == "FAIL"
            print(f"    {'ok  ' if ok else 'MISS'}  {label}"
                  f"{'' if ok else f'  -> reported {status}, expected FAIL'}")
            if ok:
                print(f"            {diags[0].get('summary')}")
            else:
                failures.append(f"NOT CAUGHT: {label} (reported {status})")

        print("\n  fragments — must NOT fail:")
        for label, body in FRAGMENT_CASES:
            status, _ = check_hcl.validate_block(tf, ws, body)
            ok = status == "fragment"
            print(f"    {'ok  ' if ok else 'MISS'}  {label}"
                  f"{'' if ok else f'  -> reported {status}, expected fragment'}")
            if not ok:
                failures.append(f"MISCLASSIFIED: {label} reported {status}, expected fragment")

        print("\n  synthesised inputs — must come out ok:")
        for label, body in SYNTHESISED_CASES:
            status, diags = check_hcl.validate_block(tf, ws, body)
            ok = status == "ok"
            summaries = [d.get("summary") for d in diags]
            detail = "" if ok else f"  -> reported {status}: {summaries}"
            print(f"    {'ok  ' if ok else 'MISS'}  {label}{detail}")
            if not ok:
                failures.append(f"NOT SYNTHESISED: {label} reported {status}")
    finally:
        shutil.rmtree(ws, ignore_errors=True)

    print()
    if failures:
        print("FAILED:")
        for f in failures:
            print(f"  x {f}")
        return 1
    print("check_hcl.py catches every planted error and passes every honest fragment")
    return 0


if __name__ == "__main__":
    sys.exit(main())
