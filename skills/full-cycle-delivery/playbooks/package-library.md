# Playbook: package-library

**Work type:** `package-library`

## Order

1. Build package before dependent apps: `npm run build:packages`
2. If new export used by apps: rebuild `infra` / package `dist` per root AGENTS.md

## Verify

```bash
./scripts/verify-scope.sh packages/<name>
```
