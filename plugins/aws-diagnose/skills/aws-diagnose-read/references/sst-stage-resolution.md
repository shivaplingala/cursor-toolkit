# Stage vs sharedStage

From `@org/infra` (`getSharedResourceStage`):

- `dev-<personal>` → shared resources often on **`dev`**
- `dev` → `dev`
- `prod` / `production` → same stage

## Scanner behavior

`scan_sst.py --stage dev-lshiva` returns:

```json
{ "stage": "dev-lshiva", "shared_stage": "dev" }
```

SSM templates with `${stage}` resolve to the **requested** stage.
Templates with `${sharedStage}` resolve to `shared_stage`.

## Runtime vs scan

Outlook `dependencies.ts` uses:

- `dependencyStage = stage || sharedStage` for **messaging queue**
- `sharedStage` for **tenant event bus**

If AWS `get_parameter` fails for personal stage, retry with `dev` (shared).

## API base URL

Always `https://{stage}.api.example.com` — the **request** stage, not shared.
