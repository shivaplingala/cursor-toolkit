# Source priority rules

Apply when merging sub-agent findings and writing recommendations.

## Priority order

1. **Official documentation** — `docs.aws.amazon.com`, Microsoft Learn, `developer.*.com` for providers
2. **Official GitHub** — AWS samples, provider SDK repositories (`aws-samples`, `aws`, org SDK repos)
3. **This repository** — `AGENTS.md`, `docs/analysis/`, channel `AGENTS.md`, existing channel impls
4. **Community** — blogs, Stack Overflow — only when official is silent; label **confidence: possible**
5. **Never** treat unsourced model output as fact — link or mark **unverified**

## Confidence tags (required on major recommendations)

| Tag | Meaning |
| --- | ------- |
| **confirmed** | Official doc + matches repo pattern or prior deploy |
| **likely** | Official doc, not yet validated in |
| **possible** | Community, inferred, or conflicting sources — needs spike |

## Citation format

Every external claim in the final report:

- URL (stable doc link preferred over blog)
- Access date: `YYYY-MM-DD`
- Doc version or "last updated" from page when visible

## Do not use as primary sources

- Random gists (secondary at best)
- Unattributed forum posts without reproducible steps
- Deprecated API pages without noting replacement
- Copy-pasted secret values (forbidden entirely)

## Tool mapping

| Need | Tool |
| ---- | ---- |
| Official API reference | WebFetch on provider doc URL from `provider-index.md` |
| SDK version-specific usage | Context7 MCP |
| Recent changes, deprecations | WebSearch + verify on official site |
| IAM actions, quotas | AWS Knowledge MCP + IAM doc link |
| Internal patterns | graphify, GitNexus, DOX chain |
