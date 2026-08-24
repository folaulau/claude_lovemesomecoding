"""Self-test for check_aws.py: does the validator actually catch anything?

A checker that passes everything is worse than no checker, because it produces a green tick.
So this feeds it 24 commands that are correct and 12 that are wrong in the ways real content is
wrong — a renamed operation, a pluralised operation, a flag that never existed, a misspelled
waiter, a service that does not exist — and fails if it lets any of them through OR if it
rejects any of the correct ones.

The two CLI customizations in check_aws.EXTRA_FLAGS were found by this test, not by reading
source: `cloudfront create-invalidation --paths` and `eks update-kubeconfig` are CLI conveniences
with no matching API shape, and a strict model-based validator rejects both until told.

    lovemesomecoding_backend/.venv/bin/python projects/aws_tutorial/tests/test_check_aws.py
"""
import sys, io
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))
import check_aws as C

models = C.Models()

GOOD = [
    "aws s3api create-bucket --bucket my-bucket --region us-west-2",
    "aws s3api put-bucket-policy --bucket b --policy file://p.json",
    "aws s3 sync ./out s3://bucket --delete --exact-timestamps",
    "aws s3 cp ./f s3://b/f --cache-control max-age=31536000 --content-type text/html",
    "aws lambda update-function-code --function-name f --zip-file fileb://f.zip",
    "aws ec2 describe-instances --filters Name=tag:Env,Values=dev --query 'Reservations[].Instances[].InstanceId'",
    "aws ec2 stop-instances --instance-ids i-abc",
    "aws ec2 wait instance-running --instance-ids i-abc",
    "aws rds start-db-instance --db-instance-identifier mydb",
    "aws rds stop-db-instance --db-instance-identifier mydb",
    "aws cloudformation deploy --template-file t.yaml --stack-name s --capabilities CAPABILITY_IAM",
    "aws cloudformation create-change-set --stack-name s --change-set-name c --template-body file://t.yaml",
    "aws iam create-role --role-name r --assume-role-policy-document file://t.json",
    "aws ssm put-parameter --name /a/b --type SecureString --value x --region us-west-2 --profile folau",
    "aws logs tail /aws/lambda/f --follow --since 1h",
    "aws ecr get-login-password --region us-west-2",
    "aws cloudfront create-invalidation --distribution-id E30YUPLP37MY9U --paths '/*'",
    "aws sqs receive-message --queue-url u --wait-time-seconds 20 --max-number-of-messages 10",
    "aws kinesis put-record --stream-name s --partition-key k --data d",
    "aws firehose create-delivery-stream --delivery-stream-name s",
    "aws eks update-kubeconfig --name c --region us-west-2",
    "aws scheduler create-schedule --name n --schedule-expression 'rate(1 day)' --flexible-time-window Mode=OFF --target x",
    "aws sts get-caller-identity --profile folau",
    "aws secretsmanager get-secret-value --secret-id s",
]

BAD = [
    ("aws s3api create-bucket --bucket b --regions us-west-2",      "misspelled flag --regions"),
    ("aws s3api create-buckets --bucket b",                          "misspelled operation"),
    ("aws s3 synk ./out s3://b",                                     "misspelled high-level cmd"),
    ("aws s3 sync ./out s3://b --exact-timestamp",                   "singular --exact-timestamp"),
    ("aws lambda update-function-code --function f --zip-file f",    "--function not --function-name"),
    ("aws ec2 wait instance-runnning --instance-ids i",              "misspelled waiter"),
    ("aws rds start-db-instances --db-instance-identifier d",        "plural operation does not exist"),
    ("aws elasticbeanstalk create-environments --application-name a","plural operation"),
    ("aws frobnicate list-things",                                   "service does not exist"),
    ("aws cloudformation deploy --template-file t --stack-nam s",    "misspelled custom flag"),
    ("aws iam create-role --role-name r --assume-policy-document f", "wrong flag name"),
    ("aws sqs receive-message --queue-url u --wait-seconds 20",      "wrong flag name"),
]

# Lines whose SHAPE is the hard part: pipes and `&&` inside quotes and $( ), which a naive
# split cuts through the middle of a quoted string. Each entry is (line, expected command count).
# The first one is a regression: it made check_aws report "No closing quotation" on a correct
# `aws kinesis put-record` in the Kinesis post.
LINES = [
    (r"""aws kinesis put-record --stream-name b --partition-key p --data "$(echo -n '{"a":1}' | base64)" """.strip(), 1),
    ("aws s3 ls | head -5", 1),
    ("cat f | aws s3 cp - s3://b/f", 1),
    ("aws sts get-caller-identity && aws s3 ls", 2),
    (r"""aws ec2 describe-instances --query "Reservations[].Instances[?State.Name=='running'].InstanceId" """.strip(), 1),
    # Regression: a quoted argument containing literal newlines. Reported "No closing quotation"
    # on a valid `aws route53 change-resource-record-sets` until _join_quoted_lines existed.
    ("aws route53 change-resource-record-sets \\\n  --hosted-zone-id Z123 \\\n  --change-batch '{\n  \"Changes\": []\n}'", 1),
    ("aws ec2 authorize-security-group-ingress --group-id sg-a --protocol tcp --port 5432 --source-group sg-b", 1),
]

print("=== shell lines that must split correctly ===")
split_bad = []
for line, expected in LINES:
    got = list(C.shell_commands(line))
    f = []
    for g in got:
        C.check_command(g, models, f, "line")
    if len(got) != expected or f:
        split_bad.append((line, got, f))
        print(f"  ✗ {line[:88]}")
        print(f"        got {len(got)} command(s), expected {expected}")
        for x in f:
            print(f"        {x}")
    else:
        print(f"  ✓ {len(got)} cmd(s): {line[:80]}")

print("\n=== commands that MUST pass ===")
fails = []
bad_pass = []
for c in GOOD:
    f = []
    C.check_command(c, models, f, "good")
    if f:
        fails.append((c, f))
        print(f"  ✗ FALSE POSITIVE: {c}")
        for x in f: print(f"        {x}")
    else:
        print(f"  ✓ {c[:100]}")

print("\n=== commands that MUST fail ===")
for c, why in BAD:
    f = []
    C.check_command(c, models, f, "bad")
    if not f:
        bad_pass.append((c, why))
        print(f"  ✗ MISSED ({why}): {c}")
    else:
        print(f"  ✓ caught ({why}): {f[0].split(': ',1)[1][:95]}")

print(f"\nfalse positives: {len(fails)}   missed errors: {len(bad_pass)}   bad splits: {len(split_bad)}")
sys.exit(1 if (fails or bad_pass or split_bad) else 0)
