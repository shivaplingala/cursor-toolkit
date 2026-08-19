# AWS Diagnosis: <one-line symptom>

**Conversation:** `<conversation_id>` (label: `<A|B|…>`)  
**Stage:** `<stage>` | **Region:** `<region>` | **Window:** `<utc range>`

## Summary

2–3 sentences: what's wrong and the most likely root cause. If resolved, name the
primary source file and function.

## Code location

Include when app logic is involved; omit for pure AWS/IAM/config issues.

| Role | File | Function / symbol | Confidence |
| ---- | ---- | ----------------- | ---------- |
| Primary | `apps/.../file.ts` | `functionName()` | confirmed / likely / possible |
| Related | `apps/.../other.ts` | `otherFn()` | likely |

- **Primary:** tie to a log line, branch, or `scan_sst.py` `handler` field.
- **Gap / wiring:** caller that should invoke vs callee that exists elsewhere.

Use `scan_sst.py` (`--topic lambda`, `--topic api`) and grep/stack traces.
Unresolved rows: note missing signal in **Open questions**.

## Evidence

### Identity & scope

```bash
python "$SKILL_ROOT/scripts/aws_read.py" sts get_caller_identity
```

### Timeline

| Step (UTC) | Component | Event | Source |
| ---------- | --------- | ----- | ------ |
| | | | |

### Sub-agent domains

List which L1/L2 gatherers ran and `status` (ok/partial/blocked).

### Commands (reproducible)

- Bullet list of read-only commands (redact tokens).

## Root cause

Specific cause with confidence: **confirmed** | **likely** | **possible**.

Rank alternatives if ambiguous.

## Suggested fix

Concrete steps for the **user** to apply. Reference **Code location** files/functions.
This skill does not apply changes.

## How to verify the fix

What should return to normal after the fix.

## Open questions / next reads

From sub-agent `gaps` and unresolved hypotheses.

---

## add-ons (when relevant)

### Message id comparison

| Channel | Message id | Same generation? |
| ------- | ---------- | ---------------- |
| Web | | |
| Email | | |

### Trace / channel

- `metadata.channel` per trace
- SFN `channel` if workflow involved
- Async push: `channelOutboundReply` in logs?

### Cross-conversation comparison

See `merge-template.md` — include only when diagnosing A vs B.
