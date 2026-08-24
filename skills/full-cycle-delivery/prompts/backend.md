# Backend (FCD prompt)

Dispatch agent **`backend-implementer`**. Skills: **backend**, **ponytail**.

Phase 2 backend design: agent **`backend-architect`** + skill **backend-architect** (FCD plugin). Merge workspace `agency-engineering/backend-architect` when present. Not this prompt.

## When

| Work | Agent / skill |
| ---- | ------------- |
| Lambda / API / channel / package / SST | **backend-implementer** + playbook |
| Progress ledger / host-tooling scripts | **backend-implementer** + `host-tooling` playbook |
| Fallback | `prompts/implementer.md` |

## Exit

Verify green (`verify-scope` or doctor) + progress row updated. Coding/impact review-fix still required for product code.
