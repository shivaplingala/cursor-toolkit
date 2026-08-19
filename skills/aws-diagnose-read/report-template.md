# Diagnosis Report Template

Copy this structure verbatim into the new report file under `.aws-details/reports/`. Fill every section. Delete the `> guidance` lines. No placeholders may remain in the final file.

---

```markdown
# AWS Diagnosis Report: <one-line symptom>

- **Date (UTC):** <YYYY-MM-DD HH:mm>
- **Author:** aws-diagnose-read skill
- **AWS Account:** <account id from sts get-caller-identity>
- **Region:** <region>
- **Stage:** <dev|staging|prod|personal>
- **Severity:** <SEV1 outage | SEV2 degraded | SEV3 minor>
- **Status:** <root cause confirmed | suspected | inconclusive>

## 1. Summary (plain language)

<3-5 sentences. What is broken, who/what it affects, what the root cause is, and the one-line fix. Written so a non-expert understands it.>

## 2. Symptom

- **Reported problem:** <what was observed>
- **First seen:** <timestamp or "unknown">
- **Affected resource(s):** <exact ARNs / names>
- **Blast radius:** <which features/tenants/users impacted>

## 3. Evidence (read-only findings)

> One subsection per piece of evidence. Include the EXACT command run and its real output (redact secrets).

### 3.1 <e.g. Lambda error logs>
- Command (READ-ONLY):
  ```bash
  <exact command>
  ```
- Output:
  ```
  <real trimmed output, key lines only>
  ```
- What this proves: <one sentence>

### 3.2 <metric / queue depth / table state / config check>
- Command (READ-ONLY):
  ```bash
  <exact command>
  ```
- Output:
  ```
  <real output>
  ```
- What this proves: <one sentence>

## 4. Root Cause

<Definite statement of the cause, tied directly to the evidence sections above by number, e.g. "Per 3.1 and 3.2, ...". If inconclusive, say exactly what is still unknown and the one read-only command needed to confirm.>

## 5. Recommended Fix (do exactly this, in order)

> Must be executable with zero thinking. Every value resolved. No placeholders. Mark each command READ-ONLY (safe) or WRITE (changes state — user runs).

### Step 1: <action>
- File to edit: `<repo-relative path>` (skip if no code change)
- Change:
  ```diff
  - <exact existing line(s)>
  + <exact new line(s)>
  ```
- Command:
  ```bash
  <exact command with real values>   # WRITE (changes state — user runs this)
  ```
- Expected result: <exact success signal, e.g. "prints { \"Status\": \"OK\" }">

### Step 2: <action>
- ... (same shape)

## 6. Verification (confirm it worked)

```bash
<exact read-only command>   # READ-ONLY (safe)
```
- Expected output: <exact value proving the issue is resolved, e.g. "ApproximateNumberOfMessages = 0">

## 7. Rollback (if the fix causes problems)

```bash
<exact command(s) to undo>   # WRITE (changes state — user runs this)
```
- Expected result: <system returns to prior state>

## 8. Blocked: missing inputs (only if any value could not be resolved)

- <missing value> — obtain with:
  ```bash
  <exact read-only command>
  ```

## 9. Prevention (optional, short)

<1-3 concrete, specific actions to stop recurrence. Reference exact files/resources. Omit if none.>
```

---

## Quality gate before saving

The report is only done when ALL are true:
- [ ] No `<...>` placeholders remain.
- [ ] Every evidence item has a real command + real output.
- [ ] Every fix step has exact file paths, exact diffs, and exact commands with real values.
- [ ] Every command is tagged READ-ONLY or WRITE.
- [ ] Verification section has an exact expected output.
- [ ] Rollback section is present.
- [ ] No forbidden hedging words ("consider", "maybe", "should probably", "etc.").
