# Agent host discovery install

User-global delivery and tooling skills are published from Cursor local plugins into other agent hosts (Claude, Codex, Antigravity/Gemini, etc.) so the same pipelines and routers are discoverable outside Cursor.

## Language

**Host discovery install**:
A scripted publish of skill, command, and rule artifacts from a canonical plugin tree into a host’s discovery paths.
_Avoid_: Plugin install, make installable, sync, deploy

**Skill**:
The skill directory tree (`SKILL.md` + supporting files) a host loads as agent instructions.
_Avoid_: Package, module, prompt pack

**Command**:
The slash- or prompt-invoked markdown entrypoint that points agents at a skill.
_Avoid_: Alias, shortcut, macro

**Rule**:
Host guidance loaded as always-on or requestable policy alongside skills. On Antigravity, one rule may exist as two file shapes (`.mdc` and stripped `.md`); see ADR 0002.
_Avoid_: Policy file, system prompt, instruction dump

**Canonical plugin tree**:
The source-of-truth directory under `~/.cursor/plugins/local/<plugin>/` from which host discovery installs are made.
_Avoid_: Copy, mirror, checkout (unless referring to Antigravity’s on-disk skill copy)

**Skill root**:
A host-specific directory under which skill trees are discovered (e.g. `~/.gemini/config/skills`).
_Avoid_: Install dir, skill path (prefer naming the concrete root)

**Antigravity**:
The Gemini-based IDE host that discovers skills under Gemini config paths; for this project it requires real skill copies (not symlinks) under both `~/.gemini/config/skills` and `~/.gemini/antigravity/skills`.
_Avoid_: Gemini-only, Google AI IDE (when meaning this host’s dual roots)

**Zed**:
IDE that discovers global skills under `~/.agents/skills/` (same Agents hub path used by other tools). Symlinks are supported; no separate Antigravity-style copy tree.
_Avoid_: Zed-only skill root, ~/.config/zed/skills (not used for agent skills)

**Qwen Code**:
CLI/editor that discovers personal skills under `~/.qwen/skills/` and custom slash commands under `~/.qwen/commands/`.
_Avoid_: project-only `.qwen/skills` for user-global publish

**DeepSeek Harness**:
Scans `~/.dsh/skills` (user-dsh) and `~/.agents/skills` (user-agents). Host discovery installs both.
_Avoid_: project `.dsh/skills` for user-global publish

**GLM / ZCode**:
GLM Coding Plan uses Claude Code discovery paths. GLM ZCode (Z.AI) uses `~/.zcode/skills/`.
_Avoid_: treating GLM Coding Plan as a separate skill root

**Copy freshness**:
Antigravity skill (and dual-format rule) copies match the canonical plugin tree only as of the last host discovery install; operators re-run the installer after plugin updates. Use `install-*.sh --check` or `fcd-doctor.sh` to detect drift.
_Avoid_: Auto-sync, watcher, live mirror, drift daemon
