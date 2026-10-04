# Session 10-aws

mode: `default`  cwd: `/Users/folaukaveinga/Github/claude_lovemesomecoding`  allowed: `Read Grep Bash(aws apigateway get-*) Bash(aws apigatewayv2 get-*) Bash(aws cloudfront get-*) Bash(aws cloudfront list-*) Bash(aws route53 list-*) Bash(aws acm list-*) Bash(aws acm describe-*) Bash(aws ce get-cost-and-usage *) Bash(aws sts get-caller-identity*) Bash(dig *)`

## Prompt

```text
CLAUDE.md lists two AWS resources left over from pocsoft.com (which moved off this account) as 'may still bill and are unverified': API Gateway custom domain d-slp5iqnci4.execute-api.us-west-2 and CloudFront d1zmyros44lee. Investigate them. Use the AWS CLI with profile folau (AWS_PROFILE is set); us-west-2 for API Gateway, CloudFront is global.

READ-ONLY. Only describe/list/get commands. Do not create, update, disable or delete anything, even if it is clearly orphaned; tell me instead. Cost Explorer calls cost $0.01 each, so use at most 3.

Tell me:
1. Do these resources still exist? What are they attached to (domains, certs, origins, stages, DNS records pointing at them)?
2. Are they costing money, and roughly how much per month? Show the numbers you based it on.
3. Is anything still using them (DNS still pointing here, traffic)?
4. Your recommendation, with the exact commands I would run to clean up, in the order I should run them, and what to check before each one. Do NOT run them.
Separate verified facts (with the command that showed them) from inference.
```

## Transcript

- **Bash** command='echo "profile=$AWS_PROFILE"; aws sts get-caller-identity --output json; echo ---V2; aws apigatewayv2 get-domain-names --region us-west-2 --output json; echo ---V1; aws apigateway get-domain-names --re'
- **Bash** command='aws cloudfront list-distributions --output json --query "DistributionList.Items[].{Id:Id,Domain:DomainName,Aliases:Aliases.Items,Enabled:Enabled,Status:Status,Origins:Origins.Items[].DomainName,Commen'
- **Bash** command='aws sts get-caller-identity --output json; echo ---V2; aws apigatewayv2 get-domain-names --region us-west-2 --output json; echo ---V1; aws apigateway get-domain-names --region us-west-2 --output json'
Both exist. Now the attachments: mappings, certs, distribution config, origins, DNS.

- **Bash** command='echo "--- v2 api mappings"; aws apigatewayv2 get-api-mappings --domain-name backend.pocsoft.com --region us-west-2 --output json\necho "--- v1 base path mappings"; aws apigateway get-base-path-mappings'
- **Bash** command='aws cloudfront get-distribution-config --id E1ECW7IDDZUUCG --output json --query "{ETag:ETag,Enabled:DistributionConfig.Enabled,Aliases:DistributionConfig.Aliases,Origins:DistributionConfig.Origins.It'
- **Bash** command='R="--region us-west-2 --output json"\necho "--- rest api"; aws apigateway get-rest-api --rest-api-id anwkjt5ckf $R --query "{name:name,created:createdDate,desc:description,endpoint:endpointConfiguratio'
- **Bash** command='echo "--- bucket region"; aws s3api get-bucket-location --bucket sushi.pocsoft.com --output json\necho "--- bucket size"; aws s3 ls s3://sushi.pocsoft.com --recursive --summarize | tail -3\necho "--- se'
Splitting into simpler calls.

- **Bash** command='aws apigateway get-rest-api --rest-api-id anwkjt5ckf --region us-west-2 --output json --query "{name:name,created:createdDate,desc:description,endpoint:endpointConfiguration.types,disableDefault:disab'
- **Bash** command='aws apigateway get-stages --rest-api-id anwkjt5ckf --region us-west-2 --output json --query "item[].{stage:stageName,deployment:deploymentId,cache:cacheClusterEnabled,cacheSize:cacheClusterSize,cacheS'
- **Bash** command='aws apigateway get-resources --rest-api-id anwkjt5ckf --region us-west-2 --output json --embed methods'
- **Bash** command='aws s3api list-buckets --output json --query "Buckets[?contains(Name,\'pocsoft\')].{Name:Name,Created:CreationDate}"'
- **Bash** command='aws cloudfront get-origin-access-control --id E3T7OQ8SA2ABV8 --output json --query "OriginAccessControl.OriginAccessControlConfig"'
- **Bash** command='aws lambda get-function-configuration --function-name backend-pocsoft-prod --region us-west-2 --output json --query "{Runtime:Runtime,Mem:MemorySize,Timeout:Timeout,LastModified:LastModified,Role:Role'
- **Bash** command='aws lambda get-policy --function-name backend-pocsoft-prod --region us-west-2 --output text --query Policy'
- **Bash** command='aws s3api get-bucket-location --bucket sushi.pocsoft.com --output json'
- **Bash** command='aws route53 list-hosted-zones --output json --query "HostedZones[].{Id:Id,Name:Name,Records:ResourceRecordSetCount,Private:Config.PrivateZone}"'
- **Bash** command='for h in backend.pocsoft.com sushi.pocsoft.com server.pocsoft.com pocsoft.com; do echo "== $h"; dig +short CNAME $h @8.8.8.8; dig +short A $h @8.8.8.8; done; echo "== NS"; dig +short NS pocsoft.com @8'
- **Bash** command='dig +noall +answer backend.pocsoft.com sushi.pocsoft.com server.pocsoft.com pocsoft.com NS pocsoft.com @8.8.8.8'
- **Bash** command='whois 216.150.1.1 | grep -iE "^(OrgName|NetName|NetRange|Organization)"'
- **Bash** command='aws cloudwatch get-metric-statistics --region us-east-1 --namespace AWS/CloudFront --metric-name Requests --dimensions Name=DistributionId,Value=E1ECW7IDDZUUCG Name=Region,Value=Global --start-time 20'
- **Bash** command='aws cloudwatch get-metric-statistics --region us-west-2 --namespace AWS/ApiGateway --metric-name Count --dimensions Name=ApiName,Value=backend-pocsoft --start-time 2026-07-06T00:00:00Z --end-time 2026'
- **Bash** command='aws ce get-cost-and-usage --region us-east-1 --time-period Start=2026-07-01,End=2026-10-01 --granularity MONTHLY --metrics UnblendedCost UsageQuantity --group-by Type=DIMENSION,Key=SERVICE --output js'
Finished the checks. Several were blocked by your permission settings (noted below), so I've stopped investigating and am writing up what I found.

# The two pocsoft.com leftovers

**In short:** both still exist and are still switched on. Neither is costing anything you'd notice: the whole account's API Gateway plus CloudFront bill for September was about half a cent. No DNS record points at either one. Cost isn't the real reason to clean up. The bigger issue is that the API behind the custom domain is still public, and some of its endpoints have no login and are named like they switch servers and a database on and off. There is also a third pocsoft.com resource the CLAUDE.md list missed: the CloudFront distribution for `server.pocsoft.com`.

## 1. Do they exist, and what's attached? (verified)

**`d-slp5iqnci4` is the API Gateway custom domain `backend.pocsoft.com`.** Shown by `aws apigateway get-domain-names` and `aws apigatewayv2 get-domain-names`.
- **Type and status:** REGIONAL, status AVAILABLE, created 2024-01-24.
- **Mapping:** `get-base-path-mappings` shows `(none)` → REST API **`anwkjt5ckf`** ("backend-pocsoft", EDGE, created 2024-01-26), stage **`prod`**. The stage has no cache cluster, so there's no hourly charge.
- **Certificate:** `acm describe-certificate` shows `d1c6bf15…` (`*.pocsoft.com`, `backend.pocsoft.com`) **EXPIRED 2024-12-21**, renewal FAILED. Its `InUseBy` entries are API Gateway's own load balancers (account 109351309407), which is how a cert attached to a custom domain normally shows up.
- **The API itself:** `get-resources --embed methods` shows every route goes to Lambda **`backend-pocsoft-prod`**, all with `authorizationType: NONE`:
  - `GET /`, `GET /latest-activity`, `GET /sushi/servers-status`
  - `POST /sushi/turnon-servers`, `POST /sushi/turnoff-servers`, `POST /sushi/turnoff-servers-on-inactivity`, `POST /turnoff-database`
- **Default endpoint:** `get-rest-api` shows `disableExecuteApiEndpoint: false`, so the default `anwkjt5ckf.execute-api…/prod/...` URL is still switched on.

**`d1zmyros44lee` is CloudFront distribution `E1ECW7IDDZUUCG`.** Shown by `aws cloudfront list-distributions` and `get-distribution-config`.
- **Settings:** alias `sushi.pocsoft.com`, **Enabled**, Deployed, PriceClass_All, last modified 2022-09-18.
- **Origin:** `sushi.pocsoft.com.s3.us-west-2.amazonaws.com`, using origin access control `E3T7OQ8SA2ABV8`.
- **Nothing else attached:** no logging, no WAF, no functions, no tags.
- **Certificate:** `a8d7f4db…` in us-east-1 (`*.pocsoft.com`, `sushi.pocsoft.com`, `sushi-api.pocsoft.com`), **EXPIRED 2024-09-18**. Its `InUseBy` lists **E1ECW7IDDZUUCG and E3KFWG5MPNJ9CK**.

**Not in the CLAUDE.md list:** `E3KFWG5MPNJ9CK` → `dkriovuf7m1i0.cloudfront.net`, alias `server.pocsoft.com`, origin `server.pocsoft.com.s3.us-west-2…`, Enabled. It shares the expired certificate above.

**DNS:**
- `aws route53 list-hosted-zones` shows only lovemesomecoding.com, pitaconcrete.com and folaukaveinga.com. There is no pocsoft.com zone in this account.
- `dig @8.8.8.8` shows pocsoft.com is served by `ns1/ns2.vercel-dns.com`. `backend.`, `sushi.` and `server.pocsoft.com` all resolve to A records in `216.150.x.x`. None of them point at `d-slp5iqnci4`, `d1zmyros44lee` or `dkriovuf7m1i0`.

## 2. Are they costing money? (verified, one Cost Explorer call out of the 3 allowed)

`aws ce get-cost-and-usage` for Jul–Sep, grouped by service, for the whole account:

| Month | API Gateway | CloudFront |
|---|---|---|
| 2026-07 | $0.000707 | $0.000105 |
| 2026-08 | $0.002872 | $0.000374 |
| 2026-09 | $0.004892 | $0.000480 |

These totals include your live lovemesomecoding API and CDN, so they're the most these leftovers could possibly cost. **Real cost: about $0.00/month.**

Inference: API Gateway custom domains, CloudFront distributions and ACM certificates have no standing charge. You only pay per request or per byte, and there's almost no traffic. One gap: I couldn't check whether the S3 buckets hold any data. Even so, S3 for the whole account was $0.32 in September.

## 3. Is anything still using them?

- **DNS (verified):** no. Every pocsoft.com name goes to Vercel.
- **Traffic (not verified):** CloudWatch metric calls were blocked by your permission settings, so I have no request counts for the distributions, the API or the Lambda.
- **Inference:** the tiny account-wide numbers suggest near-zero traffic. API Gateway cost has been climbing, though ($0.0007 → $0.0029 → $0.0049), and that could be your new admin API or bots hitting the open endpoints. The custom domain can't be reached by name anyway: DNS goes elsewhere and the certificate expired. The default URLs `d1zmyros44lee.cloudfront.net` and `anwkjt5ckf.execute-api.us-west-2.amazonaws.com/prod` still answer, though, because they don't use your certificate.

**Also blocked:** `lambda get-function-configuration` and `get-policy`, `s3api get-bucket-location` and `list-buckets`, and `whois`. So I don't know what "servers" and "database" the Lambda controls, or whether the buckets still exist. The `216.150.x.x` addresses being Vercel's is inference from the Vercel nameservers.

## 4. Recommendation

Delete all of it, including `server.pocsoft.com`. Do the API first: it's the one with a real risk, and the CloudFront side is just clutter.

**Step 0. Checks before anything else**
```bash
# What does the Lambda control? Read its env vars and role before deleting.
aws lambda get-function-configuration --function-name backend-pocsoft-prod --region us-west-2
aws lambda get-function --function-name backend-pocsoft-prod --region us-west-2   # code download URL, if you want a copy

# Confirm no traffic in the last 90 days (expect empty or near zero)
aws cloudwatch get-metric-statistics --region us-west-2 --namespace AWS/ApiGateway --metric-name Count \
  --dimensions Name=ApiName,Value=backend-pocsoft --start-time 2026-07-06T00:00:00Z --end-time 2026-10-04T00:00:00Z \
  --period 86400 --statistics Sum
aws cloudwatch get-metric-statistics --region us-east-1 --namespace AWS/CloudFront --metric-name Requests \
  --dimensions Name=DistributionId,Value=E1ECW7IDDZUUCG Name=Region,Value=Global \
  --start-time 2026-07-06T00:00:00Z --end-time 2026-10-04T00:00:00Z --period 86400 --statistics Sum
# repeat the CloudFront one with E3KFWG5MPNJ9CK

# Back up bucket contents if you care about them
aws s3 sync s3://sushi.pocsoft.com ./backup/sushi.pocsoft.com
aws s3 sync s3://server.pocsoft.com ./backup/server.pocsoft.com
```

**Step A. API Gateway side (us-west-2)**
```bash
# A1. Removes the custom domain; its base-path mapping goes with it.
#     Check first: dig shows backend.pocsoft.com isn't pointing at d-slp5iqnci4 (true today).
aws apigateway delete-domain-name --domain-name backend.pocsoft.com --region us-west-2

# A2. Closes the open endpoints. Check first: the Step 0 metrics are near zero and nothing you own calls anwkjt5ckf.
aws apigateway delete-rest-api --rest-api-id anwkjt5ckf --region us-west-2

# A3. Check first: InUseBy is now empty (it can take a few minutes after A1).
aws acm describe-certificate --region us-west-2 --certificate-arn arn:aws:acm:us-west-2:329580012644:certificate/d1c6bf15-e488-4254-aba9-295ab1b4837a --query Certificate.InUseBy
aws acm delete-certificate   --region us-west-2 --certificate-arn arn:aws:acm:us-west-2:329580012644:certificate/d1c6bf15-e488-4254-aba9-295ab1b4837a

# A4. Check first: the Lambda has no other triggers (event source mappings, EventBridge rules).
aws lambda list-event-source-mappings --function-name backend-pocsoft-prod --region us-west-2
aws lambda delete-function --function-name backend-pocsoft-prod --region us-west-2
#     Then remove its IAM role (from Step 0's Role field) and the /aws/lambda/backend-pocsoft-prod log group.
```

**Step B. CloudFront side. Repeat for `E1ECW7IDDZUUCG`, then `E3KFWG5MPNJ9CK`.** A distribution has to be disabled and finish deploying before it can be deleted.
```bash
ID=E1ECW7IDDZUUCG
aws cloudfront get-distribution-config --id $ID > /tmp/$ID.json
ETAG=$(jq -r .ETag /tmp/$ID.json)
jq '.DistributionConfig | .Enabled=false' /tmp/$ID.json > /tmp/$ID-off.json
aws cloudfront update-distribution --id $ID --if-match "$ETAG" --distribution-config file:///tmp/$ID-off.json
aws cloudfront wait distribution-deployed --id $ID          # ~5–15 min
ETAG=$(aws cloudfront get-distribution --id $ID --query ETag --output text)
aws cloudfront delete-distribution --id $ID --if-match "$ETAG"
```

**Step C. After both distributions are gone**
```bash
# C1. Each OAC: check that no remaining distribution uses it, then delete.
#     E3T7OQ8SA2ABV8 is sushi's; read server's OAC id from /tmp/E3KFWG5MPNJ9CK.json.
aws cloudfront list-distributions --query "DistributionList.Items[?Origins.Items[?OriginAccessControlId=='E3T7OQ8SA2ABV8']].Id"
aws cloudfront get-origin-access-control --id E3T7OQ8SA2ABV8 --query ETag --output text
aws cloudfront delete-origin-access-control --id E3T7OQ8SA2ABV8 --if-match <etag>

# C2. us-east-1 cert. Check first: InUseBy is empty.
aws acm describe-certificate --region us-east-1 --certificate-arn arn:aws:acm:us-east-1:329580012644:certificate/a8d7f4db-7bd9-45d5-8ebd-048615b6a9d9 --query Certificate.InUseBy
aws acm delete-certificate   --region us-east-1 --certificate-arn arn:aws:acm:us-east-1:329580012644:certificate/a8d7f4db-7bd9-45d5-8ebd-048615b6a9d9

# C3. Buckets: last step, and it can't be undone. Check first: your Step 0 backup finished.
aws s3 rb s3://sushi.pocsoft.com --force
aws s3 rb s3://server.pocsoft.com --force
```

When it's done, the CLAUDE.md line should list three resources (`backend.pocsoft.com` / `anwkjt5ckf`, `E1ECW7IDDZUUCG`, `E3KFWG5MPNJ9CK`) and say they cost about $0. I haven't changed any files.


_turns: 23, duration: 126s, cost: $0.74_

## Final answer

Finished the checks. Several were blocked by your permission settings (noted below), so I've stopped investigating and am writing up what I found.

# The two pocsoft.com leftovers

**In short:** both still exist and are still switched on. Neither is costing anything you'd notice: the whole account's API Gateway plus CloudFront bill for September was about half a cent. No DNS record points at either one. Cost isn't the real reason to clean up. The bigger issue is that the API behind the custom domain is still public, and some of its endpoints have no login and are named like they switch servers and a database on and off. There is also a third pocsoft.com resource the CLAUDE.md list missed: the CloudFront distribution for `server.pocsoft.com`.

## 1. Do they exist, and what's attached? (verified)

**`d-slp5iqnci4` is the API Gateway custom domain `backend.pocsoft.com`.** Shown by `aws apigateway get-domain-names` and `aws apigatewayv2 get-domain-names`.
- **Type and status:** REGIONAL, status AVAILABLE, created 2024-01-24.
- **Mapping:** `get-base-path-mappings` shows `(none)` → REST API **`anwkjt5ckf`** ("backend-pocsoft", EDGE, created 2024-01-26), stage **`prod`**. The stage has no cache cluster, so there's no hourly charge.
- **Certificate:** `acm describe-certificate` shows `d1c6bf15…` (`*.pocsoft.com`, `backend.pocsoft.com`) **EXPIRED 2024-12-21**, renewal FAILED. Its `InUseBy` entries are API Gateway's own load balancers (account 109351309407), which is how a cert attached to a custom domain normally shows up.
- **The API itself:** `get-resources --embed methods` shows every route goes to Lambda **`backend-pocsoft-prod`**, all with `authorizationType: NONE`:
  - `GET /`, `GET /latest-activity`, `GET /sushi/servers-status`
  - `POST /sushi/turnon-servers`, `POST /sushi/turnoff-servers`, `POST /sushi/turnoff-servers-on-inactivity`, `POST /turnoff-database`
- **Default endpoint:** `get-rest-api` shows `disableExecuteApiEndpoint: false`, so the default `anwkjt5ckf.execute-api…/prod/...` URL is still switched on.

**`d1zmyros44lee` is CloudFront distribution `E1ECW7IDDZUUCG`.** Shown by `aws cloudfront list-distributions` and `get-distribution-config`.
- **Settings:** alias `sushi.pocsoft.com`, **Enabled**, Deployed, PriceClass_All, last modified 2022-09-18.
- **Origin:** `sushi.pocsoft.com.s3.us-west-2.amazonaws.com`, using origin access control `E3T7OQ8SA2ABV8`.
- **Nothing else attached:** no logging, no WAF, no functions, no tags.
- **Certificate:** `a8d7f4db…` in us-east-1 (`*.pocsoft.com`, `sushi.pocsoft.com`, `sushi-api.pocsoft.com`), **EXPIRED 2024-09-18**. Its `InUseBy` lists **E1ECW7IDDZUUCG and E3KFWG5MPNJ9CK**.

**Not in the CLAUDE.md list:** `E3KFWG5MPNJ9CK` → `dkriovuf7m1i0.cloudfront.net`, alias `server.pocsoft.com`, origin `server.pocsoft.com.s3.us-west-2…`, Enabled. It shares the expired certificate above.

**DNS:**
- `aws route53 list-hosted-zones` shows only lovemesomecoding.com, pitaconcrete.com and folaukaveinga.com. There is no pocsoft.com zone in this account.
- `dig @8.8.8.8` shows pocsoft.com is served by `ns1/ns2.vercel-dns.com`. `backend.`, `sushi.` and `server.pocsoft.com` all resolve to A records in `216.150.x.x`. None of them point at `d-slp5iqnci4`, `d1zmyros44lee` or `dkriovuf7m1i0`.

## 2. Are they costing money? (verified, one Cost Explorer call out of the 3 allowed)

`aws ce get-cost-and-usage` for Jul–Sep, grouped by service, for the whole account:

| Month | API Gateway | CloudFront |
|---|---|---|
| 2026-07 | $0.000707 | $0.000105 |
| 2026-08 | $0.002872 | $0.000374 |
| 2026-09 | $0.004892 | $0.000480 |

These totals include your live lovemesomecoding API and CDN, so they're the most these leftovers could possibly cost. **Real cost: about $0.00/month.**

Inference: API Gateway custom domains, CloudFront distributions and ACM certificates have no standing charge. You only pay per request or per byte, and there's almost no traffic. One gap: I couldn't check whether the S3 buckets hold any data. Even so, S3 for the whole account was $0.32 in September.

## 3. Is anything still using them?

- **DNS (verified):** no. Every pocsoft.com name goes to Vercel.
- **Traffic (not verified):** CloudWatch metric calls were blocked by your permission settings, so I have no request counts for the distributions, the API or the Lambda.
- **Inference:** the tiny account-wide numbers suggest near-zero traffic. API Gateway cost has been climbing, though ($0.0007 → $0.0029 → $0.0049), and that could be your new admin API or bots hitting the open endpoints. The custom domain can't be reached by name anyway: DNS goes elsewhere and the certificate expired. The default URLs `d1zmyros44lee.cloudfront.net` and `anwkjt5ckf.execute-api.us-west-2.amazonaws.com/prod` still answer, though, because they don't use your certificate.

**Also blocked:** `lambda get-function-configuration` and `get-policy`, `s3api get-bucket-location` and `list-buckets`, and `whois`. So I don't know what "servers" and "database" the Lambda controls, or whether the buckets still exist. The `216.150.x.x` addresses being Vercel's is inference from the Vercel nameservers.

## 4. Recommendation

Delete all of it, including `server.pocsoft.com`. Do the API first: it's the one with a real risk, and the CloudFront side is just clutter.

**Step 0. Checks before anything else**
```bash
# What does the Lambda control? Read its env vars and role before deleting.
aws lambda get-function-configuration --function-name backend-pocsoft-prod --region us-west-2
aws lambda get-function --function-name backend-pocsoft-prod --region us-west-2   # code download URL, if you want a copy

# Confirm no traffic in the last 90 days (expect empty or near zero)
aws cloudwatch get-metric-statistics --region us-west-2 --namespace AWS/ApiGateway --metric-name Count \
  --dimensions Name=ApiName,Value=backend-pocsoft --start-time 2026-07-06T00:00:00Z --end-time 2026-10-04T00:00:00Z \
  --period 86400 --statistics Sum
aws cloudwatch get-metric-statistics --region us-east-1 --namespace AWS/CloudFront --metric-name Requests \
  --dimensions Name=DistributionId,Value=E1ECW7IDDZUUCG Name=Region,Value=Global \
  --start-time 2026-07-06T00:00:00Z --end-time 2026-10-04T00:00:00Z --period 86400 --statistics Sum
# repeat the CloudFront one with E3KFWG5MPNJ9CK

# Back up bucket contents if you care about them
aws s3 sync s3://sushi.pocsoft.com ./backup/sushi.pocsoft.com
aws s3 sync s3://server.pocsoft.com ./backup/server.pocsoft.com
```

**Step A. API Gateway side (us-west-2)**
```bash
# A1. Removes the custom domain; its base-path mapping goes with it.
#     Check first: dig shows backend.pocsoft.com isn't pointing at d-slp5iqnci4 (true today).
aws apigateway delete-domain-name --domain-name backend.pocsoft.com --region us-west-2

# A2. Closes the open endpoints. Check first: the Step 0 metrics are near zero and nothing you own calls anwkjt5ckf.
aws apigateway delete-rest-api --rest-api-id anwkjt5ckf --region us-west-2

# A3. Check first: InUseBy is now empty (it can take a few minutes after A1).
aws acm describe-certificate --region us-west-2 --certificate-arn arn:aws:acm:us-west-2:329580012644:certificate/d1c6bf15-e488-4254-aba9-295ab1b4837a --query Certificate.InUseBy
aws acm delete-certificate   --region us-west-2 --certificate-arn arn:aws:acm:us-west-2:329580012644:certificate/d1c6bf15-e488-4254-aba9-295ab1b4837a

# A4. Check first: the Lambda has no other triggers (event source mappings, EventBridge rules).
aws lambda list-event-source-mappings --function-name backend-pocsoft-prod --region us-west-2
aws lambda delete-function --function-name backend-pocsoft-prod --region us-west-2
#     Then remove its IAM role (from Step 0's Role field) and the /aws/lambda/backend-pocsoft-prod log group.
```

**Step B. CloudFront side. Repeat for `E1ECW7IDDZUUCG`, then `E3KFWG5MPNJ9CK`.** A distribution has to be disabled and finish deploying before it can be deleted.
```bash
ID=E1ECW7IDDZUUCG
aws cloudfront get-distribution-config --id $ID > /tmp/$ID.json
ETAG=$(jq -r .ETag /tmp/$ID.json)
jq '.DistributionConfig | .Enabled=false' /tmp/$ID.json > /tmp/$ID-off.json
aws cloudfront update-distribution --id $ID --if-match "$ETAG" --distribution-config file:///tmp/$ID-off.json
aws cloudfront wait distribution-deployed --id $ID          # ~5–15 min
ETAG=$(aws cloudfront get-distribution --id $ID --query ETag --output text)
aws cloudfront delete-distribution --id $ID --if-match "$ETAG"
```

**Step C. After both distributions are gone**
```bash
# C1. Each OAC: check that no remaining distribution uses it, then delete.
#     E3T7OQ8SA2ABV8 is sushi's; read server's OAC id from /tmp/E3KFWG5MPNJ9CK.json.
aws cloudfront list-distributions --query "DistributionList.Items[?Origins.Items[?OriginAccessControlId=='E3T7OQ8SA2ABV8']].Id"
aws cloudfront get-origin-access-control --id E3T7OQ8SA2ABV8 --query ETag --output text
aws cloudfront delete-origin-access-control --id E3T7OQ8SA2ABV8 --if-match <etag>

# C2. us-east-1 cert. Check first: InUseBy is empty.
aws acm describe-certificate --region us-east-1 --certificate-arn arn:aws:acm:us-east-1:329580012644:certificate/a8d7f4db-7bd9-45d5-8ebd-048615b6a9d9 --query Certificate.InUseBy
aws acm delete-certificate   --region us-east-1 --certificate-arn arn:aws:acm:us-east-1:329580012644:certificate/a8d7f4db-7bd9-45d5-8ebd-048615b6a9d9

# C3. Buckets: last step, and it can't be undone. Check first: your Step 0 backup finished.
aws s3 rb s3://sushi.pocsoft.com --force
aws s3 rb s3://server.pocsoft.com --force
```

When it's done, the CLAUDE.md line should list three resources (`backend.pocsoft.com` / `anwkjt5ckf`, `E1ECW7IDDZUUCG`, `E3KFWG5MPNJ9CK`) and say they cost about $0. I haven't changed any files.
