# Staff Engineering (Principal)

Global plugin: **20 staff/principal-level skills** for full-stack, AI, polyglot languages, and multi-cloud DevOps. Aligned with [agency-agents/engineering](https://github.com/msitarzewski/agency-agents/tree/main/engineering).

## Install

```bash
bash ~/.cursor/plugins/local/full-cycle-delivery/scripts/install-all-hosts.sh
# or this plugin only:
bash ~/.cursor/plugins/local/staff-engineering/scripts/install-staff-engineering.sh
bash ~/.cursor/plugins/local/staff-engineering/scripts/install-staff-engineering.sh --check
```

Publishes all 20 skills to Cursor, Claude Code, GLM (Claude + ZCode), Codex, Antigravity, Zed, OpenCode, Kilo, Kimi, Qwen Code, and DeepSeek Harness.

## Router

Load **`staff-engineering`** first, then the narrowest domain skill. See `INDEX.md`.

## FCD / FCD-V2

Phase 2 design: `staff-engineering` + domain skill + `backend-architect` (APIs/data/IAM).  
Phase 4: Ponytail + implementer agents.

## Regenerate skills

```bash
python3 scripts/generate-skills.py
```
