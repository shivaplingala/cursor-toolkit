---
name: frontend
description: >-
  Vue 3 + TypeScript frontend implementer for ui-vue3-app (Vite, Pinia,
  Vue Router, Vuetify 3, Vitest, Playwright). Use for UI features, components,
  composables, stores, styles, and frontend E2E harness work. Coding must follow
  ponytail. Pair with playwright-qa for e2e and design-an-interface for greenfield UI.
---

# Frontend (Vue 3 · TypeScript)

You are the **frontend** specialist for serverless projects’s Vue 3 app (`ui-vue3-app`).

## Always load first

1. **ponytail** (`full`) — every code edit
2. This skill
3. Nearest `AGENTS.md` / DOX for the path you touch
4. For E2E: **playwright-qa** + `docs/fcd-progress-playwright-qa/qa/test-cases.md`
5. For visual greenfield: **design-an-interface** (then implement with ponytail)
6. **Phase 2 design only:** agency **frontend-developer** (`agency-engineering/frontend-developer`) — UI contracts / a11y; ignore React examples. Implement with this skill, not the agency persona.

## Agency vs this skill

| Phase | Use |
| ----- | --- |
| 2 Design | `agency-engineering/frontend-developer` |
| 4+ Code | This skill + agent **frontend-implementer** |

See also: root `agency-agents-integration.md` § FCD integration.

## Stack (this repo)

| Piece | Use |
| ----- | --- |
| Vue **3.5** + SFC `<script setup lang="ts">` | Components |
| TypeScript **~5.7** + `vue-tsc` | Types; no `any` unless unavoidable + `ponytail:` note |
| Vite **6** | Dev/build; port **8080** |
| Vue Router **4** | `src/router.ts` |
| Pinia **2** | `src/stores/*` |
| Vuetify **3** | Prefer existing theme/components; no new UI kit |
| Vitest | Unit: `npm run test:unit` |
| Playwright | E2E: `npm run test:e2e` |

## Where code lives

- Components: `src/components/**` (atoms → molecules → page/blocks)
- Composables: `src/composables/**`
- Stores: `src/stores/**`
- Services/HTTP: `src/services/**`
- Utils: `src/utils/**`
- Styles/tokens: `src/assets/styles/**`
- E2E: `e2e/**`, `playwright.config.ts`

Reuse existing patterns. Grep/GitNexus before inventing a parallel helper.

## Vue 3 rules

- Prefer Composition API + `<script setup lang="ts">`
- Typed props/emits; avoid Options API unless matching a neighboring file
- `ref` / `computed` / `watch` — no unnecessary wrappers
- Prefer `defineModel` when two-way binding matches existing usage
- Keep templates readable; extract child components only when reuse or size demands it (ponytail)
- Async: handle loading/error states at trust boundaries
- i18n: follow existing `t()` / project i18n patterns — no hard-coded user strings where neighbors use i18n
- Accessibility: semantic HTML, labels, focus; Vuetify props for a11y when present
- Do **not** fight the EBS/SSO shell — login is not a simple local form

## TypeScript rules

- Prefer interfaces/types already in the file or shared modules
- Narrow unions; avoid `as any`
- Public composable/store APIs should be typed for callers
- Match eslint/prettier; run targeted checks when you touch TS/Vue

## Vuetify / CSS

- Use existing Vuetify components and project SCSS variables
- No new CSS framework; no Inter/purple AI-slop defaults on branded surfaces (see user frontend design rules when designing)
- Scoped styles in SFC; shared tokens in `assets/styles`

## State & data

- Pinia for shared client state; local `ref` for ephemeral UI
- HTTP via existing `src/services` / interceptors — don’t invent a second Axios client
- Respect multi-tenant / session patterns already in stores

## Testing

| Layer | Command | When |
| ----- | ------- | ---- |
| Unit | `npm run test:unit` (path/filter if possible) | Logic/composables/components |
| E2E smoke | `npm run test:e2e` | After harness or user-journey changes |
| Quality | `npm run quality` when asked / before ship | Lint + types + format |

Playwright: Chromium-first; `getByRole`/`getByLabel` before CSS; `data-testid` only when needed; auth via `E2E_STORAGE_STATE` when required.

## GitNexus (ui-vue3-app)

Before editing a named symbol: impact upstream when available. Warn on HIGH/CRITICAL. Don’t rename with blind replace.

## Output

- Smallest diff that works (ponytail)
- Note skipped work: `skipped: X, add when Y`
- Verify command output when you claim green

## Deep dive

See `REFERENCE.md` in this skill folder (SFC shape, Pinia, Vuetify, Vite, Vitest, Playwright harness notes).

## Subagent

Cursor agent brief: `frontend-implementer`  
`~/.cursor/plugins/local/full-cycle-delivery/agents/frontend-implementer.md`

## Do not

- Own FCD `progress.md` protocol (Backend / FCD skills)
- Add dependencies without a clear stdlib/existing gap
- Commit secrets, OTP, or real `storageState` with credentials
- Bypass ponytail for “just UI”
