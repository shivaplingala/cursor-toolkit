#!/usr/bin/env python3
"""
aws_read.py — Guarded, READ-ONLY AWS access for diagnostics.

This wrapper is the enforcement layer for the aws-readonly-diagnostics skill.
It calls boto3 on the user's behalf but REFUSES any operation that could create,
update, delete, or otherwise mutate state. Every call is checked against an
explicit denylist of mutating verbs and (optionally) an allowlist before it is
ever sent to AWS.

Design principle: fail closed. If an operation's safety can't be positively
established, it is rejected.

Usage:
    python aws_read.py <service> <operation> [--param Key=Value ...] [--region REGION]
    python aws_read.py logs filter_log_events \
        --param logGroupName=/aws/lambda/my-fn \
        --param startTime=1700000000000 \
        --param filterPattern=ERROR \
        --region us-east-1

    # List available read-only operations for a service:
    python aws_read.py <service> --list-ops

Credentials are read from the standard AWS environment variables / profile /
instance metadata chain. Never pass secrets on the command line. Set:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN (if temporary)
or
    AWS_PROFILE

Output: JSON on stdout. Errors: JSON {"error": ...} on stderr, non-zero exit.
"""

import argparse
import datetime
import decimal
import json
import sys

try:
    import boto3
    from botocore.config import Config
    from botocore.exceptions import ClientError, BotoCoreError, NoCredentialsError
except ImportError:
    sys.stderr.write(
        json.dumps({"error": "boto3 is not installed. Run: pip install boto3 --break-system-packages"}) + "\n"
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# Safety model
# ---------------------------------------------------------------------------
# Any operation whose name STARTS WITH one of these (case-insensitive) verbs is
# treated as mutating and rejected. boto3 operation names are PascalCase verbs
# (e.g. DeleteBucket, PutObject), exposed in snake_case to clients
# (delete_bucket, put_object). We normalize and match on the leading verb.
MUTATING_VERB_PREFIXES = {
    "put", "post", "create", "delete", "update", "modify", "remove", "set",
    "add", "attach", "detach", "associate", "disassociate", "register",
    "deregister", "enable", "disable", "start", "stop", "reboot", "run",
    "terminate", "launch", "copy", "import", "export", "restore", "purge",
    "send", "publish", "invoke", "execute", "apply", "cancel", "accept",
    "reject", "authorize", "revoke", "grant", "deny", "assign", "unassign",
    "tag", "untag", "move", "rename", "replace", "reset", "rotate", "upload",
    "download", "write", "request", "release", "allocate", "deallocate",
    "provision", "deprovision", "activate", "deactivate", "confirm", "verify",
    "subscribe", "unsubscribe", "abort", "complete", "initiate", "batch",
    "bulk", "merge", "split", "promote", "demote", "failover", "switch",
    "claim", "transfer", "increase", "decrease", "scale", "resize",
    "retire", "schedule", "deschedule", "swap", "test", "simulate",
    "report", "record", "track", "log", "emit", "trigger", "fire",
    "approve", "decline", "renew", "extend", "suspend", "resume",
    "lock", "unlock", "open", "close", "join", "leave", "connect",
    "disconnect", "pause", "play", "skip", "retry", "rerun", "redo",
    "undo", "clone", "duplicate", "fork", "branch", "commit", "push",
    "pull", "sync", "synchronize", "backfill", "ingest", "load",
    "flush", "evict", "expire", "invalidate", "refresh", "rebuild",
    "reindex", "repair", "recover", "rollback", "restart",
}

# A few read verbs that begin with otherwise-ambiguous letters but are safe.
# These are explicit reads. Anything matching here is allowed even though the
# leading token might otherwise be cautious. (Currently the read verbs below do
# not collide with the mutating set, but this list documents the allowed verbs.)
READ_VERB_PREFIXES = {
    "describe", "get", "list", "lookup", "search", "query", "scan",
    "head", "select", "filter", "view", "read", "check", "validate",
    "preview", "estimate", "generate",  # generate* in read context (e.g. generate_presigned is handled separately)
}

# Operations that are technically read but have side effects or cost/safety
# implications, or whose names are deceptive. Hard-blocked regardless of verb.
EXPLICIT_BLOCKLIST = {
    # STS GetSessionToken/GetFederationToken mint credentials — block to avoid
    # privilege chaining. GetCallerIdentity is fine and allowed below.
    ("sts", "get_session_token"),
    ("sts", "get_federation_token"),
    ("sts", "assume_role"),
    ("sts", "assume_role_with_saml"),
    ("sts", "assume_role_with_web_identity"),
    # S3 select scans data but is read-only; allowed. Presigned URL generation
    # creates a shareable credential-bearing URL — block by default.
    ("s3", "generate_presigned_url"),
    ("s3", "generate_presigned_post"),
    # KMS decrypt/encrypt perform crypto operations with cost & exposure; block.
    ("kms", "decrypt"),
    ("kms", "encrypt"),
    ("kms", "generate_data_key"),
    # Lambda invoke executes code — definitely not read-only.
    ("lambda", "invoke"),
    ("lambda", "invoke_async"),
    # SSM can run commands.
    ("ssm", "send_command"),
    ("ssm", "start_session"),
    # Some "get" operations actually generate credentials.
    ("ecr", "get_authorization_token"),
    ("ecr", "get_login_password"),
    ("eks", "get_token"),
    ("rds", "generate_db_auth_token"),
    ("cloudfront", "create_invalidation"),
}

# Explicit allow for a small set of read operations that begin with a verb in
# the cautious zone but are genuinely read-only and commonly needed.
EXPLICIT_ALLOWLIST = {
    ("sts", "get_caller_identity"),
}


def is_operation_safe(service: str, op: str):
    """Return (allowed: bool, reason: str). Fail closed."""
    key = (service.lower(), op.lower())

    if key in EXPLICIT_BLOCKLIST:
        return False, f"'{service}.{op}' is explicitly blocked: it can mutate state, run code, or mint credentials."

    if key in EXPLICIT_ALLOWLIST:
        return True, "explicitly allowed read operation"

    # Match leading verb token. boto3 client method names are snake_case.
    leading = op.lower().split("_", 1)[0]

    if leading in MUTATING_VERB_PREFIXES:
        return False, (
            f"'{service}.{op}' begins with mutating verb '{leading}'. "
            f"This skill performs READ-ONLY diagnostics; mutating operations are refused."
        )

    if leading in READ_VERB_PREFIXES:
        # generate_* is risky (presigned urls, tokens) unless whitelisted above.
        if leading == "generate":
            return False, (
                f"'{service}.{op}' uses 'generate' which often produces credentials or URLs; "
                f"blocked unless explicitly allowlisted."
            )
        return True, f"read verb '{leading}'"

    # Unknown verb — fail closed.
    return False, (
        f"'{service}.{op}' starts with unrecognized verb '{leading}'. "
        f"Failing closed for safety. If this is a legitimate read operation, "
        f"it must be added to READ_VERB_PREFIXES or EXPLICIT_ALLOWLIST after review."
    )


# ---------------------------------------------------------------------------
# JSON serialization for AWS responses (datetimes, bytes, Decimal, streams)
# ---------------------------------------------------------------------------
class AWSJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, bytes):
            try:
                return o.decode("utf-8")
            except UnicodeDecodeError:
                return f"<{len(o)} bytes, non-utf8>"
        if isinstance(o, set):
            return list(o)
        return super().default(o)


def parse_param(raw: str):
    """Parse Key=Value. Value may be JSON (for numbers/lists/objects) or string."""
    if "=" not in raw:
        raise ValueError(f"--param must be Key=Value, got: {raw}")
    k, v = raw.split("=", 1)
    # Try JSON first so numbers/bools/lists work; fall back to string.
    try:
        return k, json.loads(v)
    except (json.JSONDecodeError, ValueError):
        return k, v


def coerce_known_numeric(params: dict):
    """A few common params must be int/epoch-ms; coerce if they came as strings."""
    numeric_keys = {"startTime", "endTime", "limit", "maxResults", "MaxKeys",
                    "MaxItems", "interval", "Limit", "startFromHead"}
    for k in list(params.keys()):
        if k in numeric_keys and isinstance(params[k], str) and params[k].lstrip("-").isdigit():
            params[k] = int(params[k])
    return params


def list_read_ops(service: str, region: str):
    """Print the read-only operations available for a service."""
    client = boto3.client(service, region_name=region,
                          config=Config(retries={"max_attempts": 3}))
    ops = []
    for op in client.meta.service_model.operation_names:
        # operation_names are PascalCase; convert to the snake_case client method
        method = _pascal_to_snake(op)
        allowed, reason = is_operation_safe(service, method)
        if allowed:
            ops.append(method)
    print(json.dumps({"service": service, "read_only_operations": sorted(ops)},
                     indent=2))


def _pascal_to_snake(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i > 0 and not name[i - 1].isupper():
            out.append("_")
        out.append(ch.lower())
    # handle consecutive caps like 'S3' boundaries loosely
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description="Guarded read-only AWS access.")
    ap.add_argument("service", help="AWS service, e.g. logs, s3, ec2, cloudwatch, lambda")
    ap.add_argument("operation", nargs="?", help="boto3 client method (snake_case), e.g. filter_log_events")
    ap.add_argument("--param", action="append", default=[], help="Operation parameter as Key=Value (Value may be JSON)")
    ap.add_argument("--region", default=None, help="AWS region (defaults to env/profile region)")
    ap.add_argument("--list-ops", action="store_true", help="List read-only operations for the service and exit")
    ap.add_argument("--max-items", type=int, default=None, help="Cap total items when auto-paginating")
    ap.add_argument("--paginate", action="store_true", help="Auto-paginate and aggregate results if supported")
    args = ap.parse_args()

    region = args.region

    try:
        if args.list_ops:
            list_read_ops(args.service, region)
            return

        if not args.operation:
            sys.stderr.write(json.dumps({"error": "operation is required unless --list-ops is used"}) + "\n")
            sys.exit(2)

        allowed, reason = is_operation_safe(args.service, args.operation)
        if not allowed:
            sys.stderr.write(json.dumps({
                "error": "operation_refused",
                "service": args.service,
                "operation": args.operation,
                "reason": reason,
            }) + "\n")
            sys.exit(3)

        params = {}
        for p in args.param:
            k, v = parse_param(p)
            params[k] = v
        params = coerce_known_numeric(params)

        client = boto3.client(
            args.service,
            region_name=region,
            config=Config(retries={"max_attempts": 4, "mode": "standard"}),
        )

        method = getattr(client, args.operation, None)
        if method is None:
            sys.stderr.write(json.dumps({
                "error": "unknown_operation",
                "detail": f"{args.service} has no client method '{args.operation}'. "
                          f"Run with --list-ops to see read-only operations.",
            }) + "\n")
            sys.exit(4)

        # Auto-paginate when requested and supported.
        if args.paginate and client.can_paginate(args.operation):
            paginator = client.get_paginator(args.operation)
            pages = []
            count = 0
            for page in paginator.paginate(**params):
                page.pop("ResponseMetadata", None)
                pages.append(page)
                # crude item cap across common list keys
                if args.max_items:
                    count = sum(
                        len(v) for pg in pages for v in pg.values() if isinstance(v, list)
                    )
                    if count >= args.max_items:
                        break
            result = {"pages": pages}
        else:
            result = method(**params)
            if isinstance(result, dict):
                result.pop("ResponseMetadata", None)

        # Stream bodies (e.g. S3 get_object) need reading. Cap size to stay sane.
        if isinstance(result, dict) and "Body" in result and hasattr(result["Body"], "read"):
            raw = result["Body"].read(1024 * 256)  # 256 KB cap
            try:
                result["Body"] = raw.decode("utf-8")
            except UnicodeDecodeError:
                result["Body"] = f"<binary, {len(raw)} bytes shown of object; non-utf8>"
            result["_body_truncated_at_bytes"] = 1024 * 256

        sys.stdout.write(json.dumps(result, cls=AWSJSONEncoder, indent=2) + "\n")

    except NoCredentialsError:
        sys.stderr.write(json.dumps({
            "error": "no_credentials",
            "detail": "No AWS credentials found. Set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY "
                      "(and AWS_SESSION_TOKEN if temporary), or AWS_PROFILE.",
        }) + "\n")
        sys.exit(5)
    except ClientError as e:
        err = e.response.get("Error", {})
        sys.stderr.write(json.dumps({
            "error": "aws_client_error",
            "code": err.get("Code"),
            "message": err.get("Message"),
            "hint": "If this is AccessDenied, the read-only diagnosis is being blocked by IAM — "
                    "which is expected and safe. Ask the user to grant the relevant read permission.",
        }) + "\n")
        sys.exit(6)
    except (BotoCoreError, ValueError) as e:
        sys.stderr.write(json.dumps({"error": "execution_error", "detail": str(e)}) + "\n")
        sys.exit(7)


if __name__ == "__main__":
    main()