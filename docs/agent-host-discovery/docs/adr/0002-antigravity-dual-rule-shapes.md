# Antigravity rules ship as both `.mdc` and stripped `.md`

For Antigravity, each **rule** is written twice under `~/.gemini/config/rules/`: a Cursor-shaped `.mdc` (frontmatter preserved, matching existing neighbors like `ponytail.mdc`) and a frontmatter-stripped `.md` (matching Claude/Codex install helpers). One glossary concept; two file shapes for host quirks.

**Status:** accepted

**Considered options:** `.mdc` only; stripped `.md` only; both (chosen).

**Consequences:** Slightly more files on disk; installers must keep both shapes in sync on every host discovery install.
