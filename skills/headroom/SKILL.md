---
name: headroom
description: >-
  Compress large tool outputs, logs, JSON dumps, and search results via Headroom
  MCP before reasoning on them; retrieve originals with CCR when detail is needed.
  Use when tool output is large (roughly >2k tokens / multi-page dumps), when
  context is tight, when the user mentions Headroom/token savings/compression,
  or when a prior compression hash marker appears.
---

# Headroom (Cursor)

Local context compression for Cursor Agent. Prefer MCP tools over inventing compression.
See also global router: skill **cursor-global-tooling**.

## Tools

| Tool | When |
|------|------|
| `headroom_compress` | Before deep reasoning on large tool/file/log/JSON output |
| `headroom_retrieve` | Compressed view missed a detail; use `hash` (+ optional `query`) |
| `headroom_stats` | User asks about savings / session compression |

## When to compress

Do compress:
- Grep/search floods, build/test logs, large JSON/API arrays, long shell dumps
- Multi-page tool results you will only partially need

Do **not** compress:
- Short replies, the single file you are actively editing, tiny JSON (<~200 tokens)
- When the user needs every line of a small artifact

## Workflow

1. Large tool result arrives → call `headroom_compress` on that content
2. Reason on the compressed text
3. If a marker like `hash=…` appears and you need more → `headroom_retrieve`
4. Prefer `query` on retrieve when searching within a cached dump

## Cursor limits

- Cursor **default/subscription models** do not route through Headroom's HTTP proxy. MCP is the working path.
- **BYOK** OpenAI (Settings → Models → Override OpenAI Base URL): `http://127.0.0.1:8787/v1` with proxy running (`headroom proxy` or `headroom-cursor`).
- Proxy optional for MCP compress; needed for automatic BYOK compression and proxy-backed retrieve.

## Ops

```bash
headroom doctor
headroom proxy          # :8787
headroom-cursor         # start proxy + print Cursor BYOK steps
```
