#!/usr/bin/env python3
"""Prove every `aws …` command in this track is a real command, offline.

This is the AWS analogue of the Postgres track's check_sql.py, and it exists for the same reason:
the track is a rewrite of seven-year-old content, and the way old cloud content is wrong is not
that it fails to parse. It is that an operation was renamed, a flag was dropped, or a service
moved — and the sample still *looks* perfect. Nobody notices until a reader pastes it.

HOW IT WORKS

The AWS CLI does not hard-code its commands. It generates them from `botocore`, which ships a
service model for each of ~400 services listing every operation and every parameter, and derives
the command and flag names by `botocore.xform_name`:

    CreateBucket               -> aws s3api create-bucket
    ObjectLockEnabledForBucket -> --object-lock-enabled-for-bucket
    ACL                        -> --acl        (xform_name knows acronyms; a naive regex gives --a-c-l)

That mapping is exact and reversible, so for any `aws …` line we can prove the service exists, the
operation exists on it, and every flag is a real parameter of that operation — against the same
data the installed CLI uses, in milliseconds, with no credentials and nothing billed.

WHAT THIS DOES NOT PROVE — do not read it as more than it is:

  * Not that the command SUCCEEDS. No account, permission, quota or resource state is consulted.
  * Not that argument VALUES are valid. `--instance-type banana` passes; `--instance-typo` fails.
  * Not the CLI's own high-level commands. `aws s3 cp|sync|ls`, `cloudformation deploy|package`,
    `ecr get-login-password` and friends are CLI customizations with no botocore operation behind
    them. They are covered by CUSTOM_COMMANDS below — a declared allowlist, so an invented flag on
    `aws s3 sync` still fails, just against a table we maintain rather than against the model.
  * Nothing about console click-paths or IAM policy semantics.

It also checks the things next to the commands, because those rot too: JSON blocks must parse,
YAML blocks must parse, and a block that claims to be an IAM policy or a CloudFormation template
must have the keys that makes it one.

    projects/aws_tutorial/check_aws.py
    projects/aws_tutorial/check_aws.py --post aws-cloudformation --verbose
"""

import argparse
import html
import json
import re
import shlex
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import manifest  # noqa: E402

try:
    from botocore import xform_name
    from botocore.session import Session
except ImportError:  # pragma: no cover
    raise SystemExit(
        "botocore is not importable. Run this with the backend venv:\n"
        "  lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/check_aws.py"
    )

PRE = re.compile(r'<pre[^>]*class="language-([\w-]+)"[^>]*>(?:\s*<code[^>]*>)?(.*?)(?:</code>\s*)?</pre>',
                 re.S | re.I)

# ---------------------------------------------------------------------------
# CLI shape
# ---------------------------------------------------------------------------
# A handful of CLI command names differ from the botocore service they drive. Most match, so the
# ones that do not are worth naming individually.
#
# `aws s3api` is botocore's `s3`. The reverse is the trap: CLI `aws s3` is NOT the s3 service, it
# is the high-level file-transfer command set, so it must be treated as custom. Getting this
# backwards would validate `aws s3 sync` against the S3 API and reject a correct command.
#
# `aws deploy` is CodeDeploy — there is no `aws codedeploy`. This entry was added because the
# checker rejected a correct command in the CodeDeploy post, which is the table working as
# intended: an unknown service is reported loudly rather than skipped.
SERVICE_ALIASES = {
    "s3api": "s3",
    "deploy": "codedeploy",
    "configservice": "config",
}

# Accepted on every command, added by the CLI itself rather than by any service model.
GLOBAL_FLAGS = {
    "--region", "--profile", "--output", "--query", "--endpoint-url", "--no-verify-ssl",
    "--no-paginate", "--debug", "--version", "--color", "--ca-bundle", "--cli-read-timeout",
    "--cli-connect-timeout", "--cli-binary-format", "--no-cli-pager", "--cli-auto-prompt",
    "--no-cli-auto-prompt", "--no-sign-request",
}
# Added by the CLI to every operation that paginates, and to every operation at all.
INJECTED_FLAGS = {
    "--max-items", "--starting-token", "--page-size",
    "--generate-cli-skeleton", "--cli-input-json", "--cli-input-yaml",
}

# ---------------------------------------------------------------------------
# CLI customizations — commands with no botocore operation behind them
# ---------------------------------------------------------------------------
# Everything a post is allowed to use has to be declared here with its flags. This is deliberately
# a small, hand-maintained table: the point is that an invented flag still fails, and a table that
# quietly allowed anything would defeat the whole check.
#
# `None` for the flag set means "flags are not validated for this command" and is used only where
# the command genuinely takes an open-ended set. Keep that list short.
CUSTOM_COMMANDS = {
    ("s3", "cp"): {"--recursive", "--exclude", "--include", "--acl", "--cache-control",
                   "--content-type", "--content-encoding", "--metadata", "--metadata-directive",
                   "--storage-class", "--sse", "--sse-kms-key-id", "--dryrun", "--quiet",
                   "--only-show-errors", "--no-progress", "--expires", "--follow-symlinks",
                   "--no-follow-symlinks", "--request-payer"},
    ("s3", "sync"): {"--recursive", "--exclude", "--include", "--acl", "--cache-control",
                     "--content-type", "--content-encoding", "--metadata",
                     "--metadata-directive", "--storage-class", "--sse", "--sse-kms-key-id",
                     "--dryrun", "--quiet", "--only-show-errors", "--no-progress", "--delete",
                     "--exact-timestamps", "--size-only", "--follow-symlinks",
                     "--no-follow-symlinks"},
    ("s3", "ls"): {"--recursive", "--human-readable", "--summarize", "--page-size",
                   "--request-payer"},
    ("s3", "mb"): set(),
    ("s3", "rb"): {"--force"},
    ("s3", "rm"): {"--recursive", "--exclude", "--include", "--dryrun", "--quiet",
                   "--only-show-errors"},
    ("s3", "mv"): {"--recursive", "--exclude", "--include", "--acl", "--dryrun", "--quiet"},
    ("s3", "presign"): {"--expires-in"},
    ("s3", "website"): {"--index-document", "--error-document"},

    ("cloudformation", "deploy"): {"--template-file", "--stack-name", "--parameter-overrides",
                                   "--capabilities", "--no-execute-changeset", "--role-arn",
                                   "--notification-arns", "--fail-on-empty-changeset",
                                   "--no-fail-on-empty-changeset", "--tags", "--force-upload",
                                   "--s3-bucket", "--s3-prefix", "--kms-key-id",
                                   "--disable-rollback", "--on-failure"},
    ("cloudformation", "package"): {"--template-file", "--s3-bucket", "--s3-prefix",
                                    "--kms-key-id", "--output-template-file", "--use-json",
                                    "--force-upload", "--metadata"},

    ("ecr", "get-login-password"): set(),

    ("configure", "list"): set(),
    ("configure", "set"): set(),
    ("configure", "get"): set(),
    ("configure", "sso"): set(),

    ("sso", "login"): {"--sso-session"},
    ("sso", "logout"): set(),

    ("logs", "tail"): {"--follow", "--since", "--format", "--filter-pattern",
                       "--log-stream-names", "--log-stream-name-prefix"},

    ("deploy", "push"): {"--application-name", "--s3-location", "--ignore-hidden-files",
                         "--no-ignore-hidden-files", "--source", "--description"},

    ("eks", "update-kubeconfig"): {"--name", "--kubeconfig", "--role-arn", "--dry-run",
                                   "--verbose", "--alias", "--user-alias"},
}

# Operations that DO exist in botocore but where the CLI adds convenience flags on top of the API
# shape. `create-invalidation` is the one everybody meets: the API takes a nested
# `--invalidation-batch` structure, and the CLI lets you write `--paths '/*'` instead.
#
# Both entries here were found by the self-test in tests/ rather than by reading the source — a
# validator this strict produces false positives, and the false positives are the interesting
# output. Add to this table only when the real CLI genuinely accepts the flag.
_SG_SHORTHAND = {"--protocol", "--port", "--cidr", "--source-group"}

EXTRA_FLAGS = {
    ("cloudfront", "create-invalidation"): {"--paths"},
    ("cloudfront", "create-distribution"): {"--origin-domain-name", "--default-root-object"},
    # The security-group rule commands take a nested --ip-permissions structure in the API, and
    # the CLI adds a flat shorthand for the common single-rule case. Verified against
    # `aws ec2 authorize-security-group-ingress help` on aws-cli/2.32.24 — all four commands
    # accept the same four flags.
    ("ec2", "authorize-security-group-ingress"): _SG_SHORTHAND,
    ("ec2", "authorize-security-group-egress"): _SG_SHORTHAND,
    ("ec2", "revoke-security-group-ingress"): _SG_SHORTHAND,
    ("ec2", "revoke-security-group-egress"): _SG_SHORTHAND,
}

# CLI command groups that are valid with no subcommand at all, only flags.
BARE_COMMAND_GROUPS = {"configure", "help"}

# Commands whose second token is a CLI verb rather than an operation.
#   aws ec2 wait instance-running --instance-ids i-abc
# `wait` is generated from the service's waiter model, so the waiter name is checked against it.
WAIT = "wait"

# Languages whose blocks are parsed as data rather than as shell.
JSON_LANGS = {"json"}
YAML_LANGS = {"yaml", "yml"}
SHELL_LANGS = {"bash", "shell", "sh"}


class Models:
    """Lazily loaded botocore service models, cached per service."""

    def __init__(self):
        self.session = Session()
        self.available = set(self.session.get_available_services())
        self._cache = {}
        # An alias pointing at a service that does not exist is worse than no alias: the command
        # is reported as "no such service" naming the CLI spelling, so the message blames the post
        # rather than this table. Caught exactly that with `iot-data -> iot-data-plane`, which was
        # a guess — botocore calls it `iot-data` and needed no alias at all.
        broken = {k: v for k, v in SERVICE_ALIASES.items() if v not in self.available}
        if broken:
            raise SystemExit(
                "SERVICE_ALIASES points at services botocore does not have: "
                + ", ".join(f"{k} -> {v}" for k, v in sorted(broken.items())))

    def get(self, service):
        if service not in self._cache:
            try:
                self._cache[service] = self.session.get_service_model(service)
            except Exception:
                self._cache[service] = None
        return self._cache[service]

    def operations(self, service):
        """CLI operation name -> botocore operation name."""
        model = self.get(service)
        if model is None:
            return {}
        return {xform_name(op).replace("_", "-"): op for op in model.operation_names}

    def flags(self, service, operation):
        """The set of `--flag` names valid for this operation."""
        model = self.get(service)
        op = model.operation_model(operation)
        shape = op.input_shape
        if shape is None:
            return set()
        return {"--" + xform_name(m).replace("_", "-") for m in shape.members}

    def waiters(self, service):
        try:
            return {xform_name(w).replace("_", "-")
                    for w in self.session.get_waiter_model(service).waiter_names}
        except Exception:
            return set()


def split_top_level(line):
    """Split a shell line on `|`, `||`, `&&` and `;` — but only at the top level.

    ⚠️ A naive `re.split(r'\\||&&|;', line)` is wrong, and wrong in a way that looks fine until a
    post contains a perfectly ordinary command:

        aws kinesis put-record --data "$(echo -n '{"a":1}' | base64)"

    Splitting on that inner `|` cuts the line in half through the middle of a quoted string, and
    shlex then fails with "No closing quotation" — reported as a broken sample when the sample is
    correct. So this tracks quotes and `$( )` depth and only breaks outside both.
    """
    parts, buf = [], []
    quote = None
    depth = 0
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            buf.append(ch)
            if ch == "\\" and i + 1 < len(line):
                buf.append(line[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
            buf.append(ch)
        elif ch == "$" and line[i:i + 2] == "$(":
            depth += 1
            buf.append(ch)
        elif ch == "(" and depth:
            depth += 1
            buf.append(ch)
        elif ch == ")" and depth:
            depth -= 1
            buf.append(ch)
        elif depth == 0 and ch in "|;&":
            run = len(line[i:]) - len(line[i:].lstrip(ch))
            parts.append("".join(buf))
            buf = []
            i += run
            continue
        else:
            buf.append(ch)
        i += 1
    parts.append("".join(buf))
    return parts


def _unclosed_quote(line, quote):
    """The quote character still open at the end of `line`, given one open at the start."""
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            if ch == "\\" and quote == '"':
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "#" and quote is None and (i == 0 or line[i - 1].isspace()):
            break  # a comment cannot open a quote
        i += 1
    return quote


def _join_quoted_lines(lines):
    """Re-join lines that are inside a quoted argument spanning newlines.

    ⚠️ A shell argument may contain literal newlines, and `aws` commands taking inline JSON
    routinely do:

        aws route53 change-resource-record-sets --change-batch '{
          "Changes": [...]
        }'

    Splitting that on newlines hands shlex a fragment ending in an unterminated quote, reported as
    "No closing quotation" on a perfectly valid sample. Backslash continuations were already
    handled; this is the other way a command spans lines.
    """
    out, buf, quote = [], [], None
    for line in lines:
        if quote:
            buf.append(line)
        else:
            buf = [line]
        quote = _unclosed_quote(line, quote)
        if not quote:
            out.append("\n".join(buf))
            buf = []
    if buf:
        out.append("\n".join(buf))
    return out


def shell_commands(block):
    """Yield each `aws …` invocation in a shell block, line continuations joined.

    Comments are stripped, but only a `#` that starts a line or follows whitespace — a `#` inside
    a URL fragment or a JMESPath expression is not a comment.
    """
    text = re.sub(r"\\\n\s*", " ", block)
    for line in _join_quoted_lines(text.splitlines()):
        line = re.sub(r"(^|\s)#.*$", "", line).strip()
        if not line:
            continue
        # Look for `aws` at the start of any pipeline segment, so `… | aws s3 cp - s3://…` is
        # checked too, and a leading `$ ` prompt is tolerated.
        for segment in split_top_level(line):
            segment = segment.strip()
            if segment.startswith("$ "):
                segment = segment[2:].strip()
            if re.match(r"^aws\s", segment):
                yield segment


def check_command(command, models, findings, where):
    try:
        tokens = shlex.split(command, comments=False)
    except ValueError as exc:
        findings.append(f"{where}: cannot tokenize {command!r} ({exc})")
        return None

    if len(tokens) < 2:
        findings.append(f"{where}: bare `aws` with no service: {command!r}")
        return None

    cli_service = tokens[1]
    rest = tokens[2:]

    if cli_service in {"help", "--version", "--help"}:
        return "ok"

    # `aws configure` is a CLI command group with no service behind it, and unlike `aws s3` its
    # BARE form is valid — `aws configure --profile x` runs the interactive prompt. So it cannot
    # be matched by the (service, subcommand) table below, which needs a subcommand to key on.
    if cli_service in BARE_COMMAND_GROUPS and (not rest or rest[0].startswith("-")):
        return "custom"

    # `aws s3 cp` and friends: a CLI customization, checked against the declared table.
    if rest and (cli_service, rest[0]) in CUSTOM_COMMANDS:
        allowed = CUSTOM_COMMANDS[(cli_service, rest[0])]
        if allowed is None:
            return "custom"
        for flag in re.findall(r"(?<![\w-])--[a-z0-9][a-z0-9-]*", " ".join(rest[1:])):
            if flag not in allowed and flag not in GLOBAL_FLAGS:
                findings.append(
                    f"{where}: `aws {cli_service} {rest[0]}` has no flag {flag} "
                    f"(CLI customization; allowed flags are declared in check_aws.py)")
        return "custom"

    service = SERVICE_ALIASES.get(cli_service, cli_service)

    # CLI `aws s3` is the high-level command set, not the S3 API. If it got here, the subcommand
    # is not one we declared — that is the finding, not "operation not found on the s3 model".
    if cli_service == "s3":
        shown = f"aws s3 {rest[0]}" if rest else "aws s3"
        findings.append(
            f"{where}: `{shown}` is not a high-level s3 command. Did you mean `aws s3api`?")
        return None

    if service not in models.available:
        findings.append(f"{where}: no such AWS service `{cli_service}` in botocore "
                        f"{models.session.user_agent_version if hasattr(models.session, 'user_agent_version') else ''}"
                        .rstrip())
        return None

    if not rest:
        findings.append(f"{where}: `aws {cli_service}` with no operation")
        return None

    # `aws ec2 wait instance-running`
    if rest[0] == WAIT:
        if len(rest) < 2:
            findings.append(f"{where}: `aws {cli_service} wait` with no waiter name")
            return None
        waiters = models.waiters(service)
        if rest[1] not in waiters:
            findings.append(
                f"{where}: `{cli_service}` has no waiter `{rest[1]}`"
                + (f" — closest: {_closest(rest[1], waiters)}" if waiters else ""))
        return "waiter"

    operations = models.operations(service)
    cli_op = rest[0]
    if cli_op in {"help", "wait"}:
        return "ok"
    if cli_op not in operations:
        findings.append(
            f"{where}: `{cli_service}` has no operation `{cli_op}`"
            + (f" — closest: {_closest(cli_op, set(operations))}" if operations else ""))
        return None

    valid = (models.flags(service, operations[cli_op]) | GLOBAL_FLAGS | INJECTED_FLAGS
             | EXTRA_FLAGS.get((service, cli_op), set()))
    # A boolean member `X` also generates `--no-x`.
    valid |= {f.replace("--", "--no-", 1) for f in valid}

    for flag in re.findall(r"(?<![\w-])--[a-z0-9][a-z0-9-]*", " ".join(rest[1:])):
        if flag not in valid:
            findings.append(
                f"{where}: `aws {cli_service} {cli_op}` has no parameter {flag}"
                + (f" — closest: {_closest(flag, valid)}" if valid else ""))
    return "ok"


def _closest(needle, haystack):
    import difflib
    match = difflib.get_close_matches(needle, sorted(haystack), n=1, cutoff=0.6)
    return match[0] if match else "no close match"


def check_data_block(lang, block, findings, where):
    """JSON and YAML blocks must parse, and declare what they claim to be."""
    text = block.strip()
    if lang in JSON_LANGS:
        # A fragment shown to illustrate shape is allowed to elide with `...` or a comment; a
        # block that does neither is expected to be complete and valid.
        if "..." in text or "…" in text:
            return "fragment"
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            findings.append(f"{where}: JSON block does not parse — {exc}")
            return None
        if isinstance(parsed, dict) and "Statement" in parsed:
            if parsed.get("Version") != "2012-10-17":
                findings.append(
                    f"{where}: IAM policy has Version {parsed.get('Version')!r}. The only value "
                    "AWS accepts is '2012-10-17' — '2008-10-17' silently disables policy variables.")
            for i, st in enumerate(parsed["Statement"] if isinstance(parsed["Statement"], list)
                                   else [parsed["Statement"]]):
                if "Effect" not in st:
                    findings.append(f"{where}: IAM policy statement {i} has no Effect")
                if st.get("Effect") not in (None, "Allow", "Deny"):
                    findings.append(
                        f"{where}: IAM policy statement {i} Effect is {st['Effect']!r}, "
                        "must be Allow or Deny")
                if "Action" not in st and "NotAction" not in st:
                    findings.append(f"{where}: IAM policy statement {i} has neither Action "
                                    "nor NotAction")
        return "json"

    if lang in YAML_LANGS:
        try:
            import yaml
        except ImportError:
            return "yaml-unchecked"
        # CloudFormation short forms (!Ref, !GetAtt, !Sub) are not standard YAML tags, so a plain
        # safe_load rejects a perfectly valid template. Register them as opaque scalars/sequences.
        class CfnLoader(yaml.SafeLoader):
            pass

        def _opaque(loader, node):
            if isinstance(node, yaml.ScalarNode):
                return loader.construct_scalar(node)
            if isinstance(node, yaml.SequenceNode):
                return loader.construct_sequence(node)
            return loader.construct_mapping(node)

        for tag in ("Ref", "GetAtt", "Sub", "Join", "Select", "Split", "ImportValue", "If",
                    "Equals", "Not", "And", "Or", "FindInMap", "Base64", "Cidr", "GetAZs",
                    "Condition", "Transform"):
            CfnLoader.add_constructor("!" + tag, _opaque)
        try:
            parsed = yaml.load(text, Loader=CfnLoader)
        except yaml.YAMLError as exc:
            findings.append(f"{where}: YAML block does not parse — "
                            f"{str(exc).splitlines()[0] if str(exc) else exc}")
            return None
        if isinstance(parsed, dict) and "Resources" in parsed:
            for name, res in (parsed["Resources"] or {}).items():
                if not isinstance(res, dict) or "Type" not in res:
                    findings.append(f"{where}: CloudFormation resource {name} has no Type")
        return "yaml"
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--post", default=None, help="check one slug instead of the track")
    parser.add_argument("--verbose", action="store_true", help="print every command checked")
    args = parser.parse_args()

    entries = manifest.POSTS
    if args.post:
        entries = [e for e in manifest.POSTS if e["slug"] == args.post]
        if not entries:
            raise SystemExit(f"not in the manifest: {args.post}")

    models = Models()
    findings = []
    missing = []
    checked = {"aws": 0, "custom": 0, "waiter": 0, "json": 0, "yaml": 0}
    written = 0

    print(f"botocore models: {len(models.available)} services\n")

    for entry in entries:
        path = HERE / "posts" / entry["file"]
        if not path.exists():
            missing.append(entry["slug"])
            continue
        written += 1
        raw = path.read_text(encoding="utf-8")
        before = len(findings)
        per_post = {"aws": 0, "custom": 0, "waiter": 0, "json": 0, "yaml": 0}

        for lang, block in PRE.findall(raw):
            block = html.unescape(block)
            where = f"{entry['slug']}"
            if lang in SHELL_LANGS:
                for command in shell_commands(block):
                    kind = check_command(command, models, findings, where)
                    if args.verbose:
                        mark = "  " if kind else "✗ "
                        print(f"  {mark}{command[:130]}")
                    if kind in ("ok",):
                        per_post["aws"] += 1
                    elif kind in ("custom", "waiter"):
                        per_post[kind] += 1
            elif lang in JSON_LANGS | YAML_LANGS:
                kind = check_data_block(lang, block, findings, where)
                if kind in ("json", "yaml"):
                    per_post[kind] += 1

        for k, v in per_post.items():
            checked[k] += v
        status = "✗" if len(findings) > before else "✓"
        parts = [f"{v} {k}" for k, v in per_post.items() if v]
        print(f"  {status} {entry['slug']:<40} {', '.join(parts) if parts else 'no samples'}")

    print()
    total = sum(checked.values())
    print(f"checked {total} sample(s) across {written} post(s): "
          + ", ".join(f"{v} {k}" for k, v in checked.items() if v))

    for slug in missing:
        print(f"  not written: {slug}")

    if findings:
        print(f"\n{len(findings)} FAILURE(S):")
        for f in findings:
            print(f"  ✗ {f}")
        return 1

    if missing:
        print(f"\nno failures in the {written} written post(s); {len(missing)} still to write.")
    else:
        print(f"\nall {written} posts pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
