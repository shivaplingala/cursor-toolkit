# Subagent: pre-ship reviewer

**Role:** Full PR readiness before human merge.

## Inputs

- Full diff vs base branch
- Plan path + completion status
- Work type

## Checklist

- [ ] All plan tasks checked
- [ ] `./scripts/verify-scope.sh` green for touched workspaces (or `--affected`)
- [ ] `npm run quality` output pasted (or `quality:full` for large features)
- [ ] Review matrix rows applied (security, GitNexus, DOX, channel plug-in, etc.)
- [ ] No secrets in diff
- [ ] CI jobs mirror local verify

## Output

`SHIP READY` or `BLOCKED` with numbered items.

**Forbidden:** claim CI-equivalent green without command output.
