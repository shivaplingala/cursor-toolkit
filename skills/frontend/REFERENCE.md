# Frontend reference — Vue 3 · TypeScript · Vite

Companion to `SKILL.md`. Prefer repo patterns over inventing new ones.

## Component shape

```vue
<script setup lang="ts">
import { computed, ref } from 'vue'

const props = defineProps<{
  title: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  select: [id: string]
}>()

const open = ref(false)
const label = computed(() => props.title.trim())
</script>

<template>
  <v-btn :disabled="disabled" @click="emit('select', 'x')">
    {{ label }}
  </v-btn>
</template>
```

- One concern per SFC; extract when file fights readability
- Prefer typed `defineProps` / `defineEmits` over runtime-only props
- `v-model` → `defineModel` when the codebase already uses it nearby

## Composables

- Name `useX`; return a plain object of refs/fns
- Side effects in `onMounted` / `watch` with cleanup
- Don’t put HTTP in every composable — call `src/services` helpers

## Pinia

- Setup stores (`defineStore('id', () => { … })`) when neighbors use them
- Actions async; catch and surface errors (toast/store flag) — don’t swallow
- Selectors as `computed` inside store or thin wrappers outside

## Router

- Named routes when already used; lazy `() => import(…)` for heavy pages
- Guards: match existing auth/tenant patterns — don’t add a second gate

## Vuetify 3

- Prefer `v-btn`, `v-text-field`, `v-select`, `v-data-table`, layout grids already in the page
- Density / variant: copy siblings on the same screen
- Icons: existing set only
- Dialogs: keep focus trap / close on escape via Vuetify defaults

## Forms & validation

- Reuse existing form helpers / Vuetify rules patterns
- Disable submit while pending; clear errors on change when neighbors do

## Performance (lazy defaults)

- Don’t add `v-memo` / virtual lists unless measured need
- Prefer `v-if` vs `v-show` correctly (mount cost vs toggle cost)
- Images: existing lazy/CDN patterns

## TypeScript pitfalls (Vue)

- Template refs: `useTemplateRef` / typed `Ref<HTMLElement | null>` per project style
- Generic components: follow existing `vue-tsc` patterns; don’t silence with `@ts-ignore`
- Prop drilling past 2 levels → consider provide/inject or store (only if already the local pattern)

## Vite

- Env: `import.meta.env.VITE_*` only; never commit secrets
- Alias `@/` → `src/` as configured
- Dev server **8080** — Playwright `webServer` uses this

## Vitest

- Co-locate or `__tests__` matching neighbors
- Prefer testing composable/pure logic over brittle snapshot of full Vuetify trees
- `mount`/`shallowMount` patterns from existing tests

## Playwright (UI harness)

- Locators: role → label → text → test id
- Auth: `storageState` / `E2E_STORAGE_STATE` — never invent OTP login in CI
- Smoke lives in `e2e/`; keep journeys mapped in `playwright-id-map.md` when under FCD delivery

## Design (when inventing UI)

- User frontend design rules apply (brand-first, no card spam, no purple AI defaults)
- Inside existing product chrome: **match the app**, don’t redesign

## Anti-patterns

- New state library next to Pinia
- Options API islands in Composition API trees without cause
- Global CSS that fights Vuetify theme
- `any` to silence vue-tsc
- E2E that re-implements unit tests
