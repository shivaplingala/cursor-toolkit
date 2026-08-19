# Playbook: bug-design-investigation

Research type: `bug-design-investigation`

Design investigation before coding a fix — root-cause hypotheses, provider docs, code paths. **No code in output.**

## Checklist

- [ ] Symptom and reproduction steps (from intake)
- [ ] Affected workspace(s) and user-visible impact
- [ ] Internal trace: GitNexus execution flows, graphify path from entrypoint to failure
- [ ] Similar fixes or issues in repo (grep, git history if relevant)
- [ ] External: provider/SDK docs if provider-related symptom
- [ ] Optional: `aws-diagnose-read` appendix when **live AWS evidence** needed (logs, traces, S3)
- [ ] Root-cause hypotheses ranked with confidence
- [ ] Recommended fix approach — **minimal diff, Ponytail alignment**
- [ ] Blast radius if touching shared symbols (`gitnexus_impact`)
- [ ] Regression test ideas (no test code — describe cases)
- [ ] Open questions if evidence insufficient

## Distinction from aws-diagnose-read

| This playbook | aws-diagnose-read |
| ------------- | ----------------- |
| Design before fix; may use static code + docs | Live account evidence after deploy |
| Hypotheses + recommended approach | Timeline + root cause from logs |
| Can run without AWS credentials | Requires DIAG_TOKEN / AWS read access |

Run both in parallel when intake requests live state.

## Report emphasis

- Hypothesis table: | Hypothesis | Evidence | Confidence | Test to confirm |
- **Recommended fix approach** — one primary, alternatives only if close call
- Explicit "do not implement until Approved"

## Sub-agent focus

| Sub-agent | Extra focus |
| --------- | ----------- |
| external-docs | Provider error codes, known issues |
| github-samples | Provider SDK issues; repo prior art |
| aws-config-catalog | Config mismatch hypotheses (SSM path, IAM) |
| codebase | Primary — code path, callers, learned facts |
