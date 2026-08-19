# SST scan sub-agent (readonly)

```markdown
SST SCAN SUB-AGENT (aws-diagnose-read phase 0.5)

Read-only filesystem scan — do NOT call AWS.

python "$SKILL_ROOT/scripts/scan_sst.py" \
  --app {{APP}} \
  --topic {{TOPIC}} \
  --search "{{SEARCH}}" \
  --stage {{STAGE}} \
  --json

Return CLI JSON only. No reports. No fix suggestions.
```

`subagent_type`: `shell`, `readonly: true`, fast model.
