# internal research checklist

Mandatory for every report via `codebase` sub-agent.

## DOX chain (read before citing paths)

Walk in order for every target path:

1. Root `AGENTS.md` — learned preferences, skill index, workspace facts
2. `apps/AGENTS.md` — app boundaries
3. Nearest app or channel `AGENTS.md` (e.g. `apps/channels/outlook/AGENTS.md`)
4. Package `AGENTS.md` if UI/libs touched (e.g. `packages/outlook-admin-ui/AGENTS.md`)

## graphify (mandatory before Read/Grep on unfamiliar areas)

```bash
graphify query "<task in natural language>"
graphify explain "<concept>"    # e.g. channelOutboundReply, ASYNC_PUSH_CHANNELS
graphify path "<symbol A>" "<symbol B>"   # dependency path
```

If `graphify-out/graph.json` missing, note gap and use GitNexus + grep.

## GitNexus (mandatory for shared symbols)

Before recommending edits to shared functions:

```text
gitnexus_query({ query: "<concept>" })
gitnexus_context({ name: "<symbolName>" })
gitnexus_impact({ target: "<symbolName>", direction: "upstream" })
```

Report blast radius (callers, execution flows, risk level) in **codebase mapping**.

## Key internal docs by task type

| Doc | When |
| --- | ---- |
| `docs/analysis/async-channel-push-extensibility-review.md` | Any async channel |
| `docs/analysis/async-channel-push-routing-plan.md` | Channel routing / workflow push |
| `docs/analysis/channel-async-delivery-architecture.md` | Multi-surface delivery |
| `apps/channels/outlook/AGENTS.md` | Reference outbound consumer |
| `skills-agents-autos-plans/FULL-CYCLE-DELIVERY-PLAN.md` | Implementation phase gates (do not run now) |

## Channel matrix

- Allowed channels: `ALLOWED_CHANNELS` in `apps/conversation-service/src/utils/security/input-validation.ts`
- Async push set: `ASYNC_PUSH_CHANNELS` in channel routing (grep `channel-routing.ts`)
- Integration channels: **no** `channelOutboundReply` unless product adds callback

## Reference implementations

| Pattern | Reference path |
| ------- | -------------- |
| Async push channel (email) | `apps/channels/outlook/` |
| Slack / Teams | `apps/channels/slack/`, `apps/channels/teams/` |
| Shared outbound utils | `apps/channels/shared/utils/outbound` |
| Workflow channel prompts | `apps/conversation-service/src/prompts/agentic-workflow/` |
| Shared SQS queue | `apps/tenant-management/sst/stacks/messaging-queue-stack.ts` |

## Learned preferences to respect (from root AGENTS.md)

- SST deploy-time config over runtime SSM/Secrets writes
- Shared channel queue from tenant-management messaging stack
- conversation-service errors: primary text in JSON `error` field
- Workflow: SFN `channel` for prompts; `session.channel` for async delivery
- Outlook-specific rules only when researching Outlook

## Deliverable fields (for sub-agent JSON)

- `paths_to_extend[]` — file paths, reuse vs new, notes
- `patterns_to_reuse[]` — symbol or module, reference channel
- `blast_radius` — GitNexus summary if shared symbols involved
- `conflicts[]` — contradicts learned preferences or existing design
- `gaps[]` — could not verify internally
