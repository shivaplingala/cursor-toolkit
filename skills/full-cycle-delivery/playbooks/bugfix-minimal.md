# Playbook: bugfix-minimal

**Work type:** `bugfix-minimal`  
**Persona:** Ponytail only — no agency Minimal Change Engineer.

## Checklist

- [ ] Trace root cause end-to-end (symptom ≠ cause)
- [ ] Grep all callers of shared function; fix once at source
- [ ] GitNexus impact if touching shared symbols
- [ ] Smallest diff that fixes root cause
- [ ] Unit test or assert-based check if non-trivial logic
- [ ] `./scripts/verify-scope.sh <touched-workspace>`
- [ ] Skip full architecture unless systemic flaw → ADR follow-up

## Skip

- research-agent (unless provider docs needed)
- Full ADR unless design flaw exposed

## Verify

When touching **serverless-monorepo** workspaces:

```bash
./scripts/verify-scope.sh apps/<app>
```

When the fix is only **user-global plugins / install scripts**, use work type `host-tooling` instead (or verify with that plugin’s `install-*.sh --check` / `scripts/fcd-doctor.sh`). Do not invent a green `verify-scope` for paths outside the monorepo.