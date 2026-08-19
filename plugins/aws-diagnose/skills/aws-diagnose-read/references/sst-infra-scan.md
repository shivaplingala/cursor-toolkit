# SST infrastructure scan (phase 0.5)

Static read of `apps/**/sst.config.ts` and `sst/stacks/**` — no AWS calls.

## CLI

```bash
SCAN="$SKILL_ROOT/scripts/scan_sst.py"

python $SCAN --list-apps --json
python $SCAN --app conversation-service --topic api --json
python $SCAN --app channels/outlook --topic lambda --stage dev-lshiva --json
python $SCAN --topic ssm --search messaging --stage dev-lshiva --json
python $SCAN --search outbound --stage dev-lshiva --json
python $SCAN --refresh-cache   # after SST stack edits
```

Cache: `cache/manifest.json` under this skill directory.

## Query topics

| Need | Flags |
| ---- | ----- |
| Lambda + log group hint | `--topic lambda --stage STAGE` |
| SSM paths | `--topic ssm --stage STAGE` |
| API routes | `--topic api` |
| Queues | `--topic queue` |
| Stack files | `--topic stacks --app APP` |

## email/web minimum scans

```bash
python $SCAN --app conversation-service --topic lambda --stage STAGE --json
python $SCAN --app channels/outlook --topic lambda --stage STAGE --json
python $SCAN --app workflow --search RunAgent --stage STAGE --json
```

Pass `log_group_hint`, `handler`, `file`, and `resolved_path` into L2 sub-agent prompts.

## AWS → code (after scan)

| Scan field | Use |
| ---------- | --- |
| `functions[].handler` | Source file (`src/handlers/...`) |
| `functions[].file` | SST stack that defines the Lambda |
| `routes[].route_key` + `file` | API handler location |
| `ssm_parameters[].file` | Who publishes the parameter |

Combine with CloudWatch stack traces for **Code location** in reports.

## Limitations

- Static source only — deployed Pulumi names may differ slightly.
- Cross-app deps in `dependencies.ts` may read SSM without defining it — scan the owning app.
- Traces bucket is often `TRACES_BUCKET_NAME` env, not SSM — use live AWS or message API.
