# Antigravity skills are real copies

Antigravity/Gemini skill discovery has historically failed to follow symlinked skill trees under some roots. Host discovery install therefore `rsync`s the canonical plugin skill into both `~/.gemini/config/skills/<name>/` and `~/.gemini/antigravity/skills/<name>/` instead of `ln -s`.

**Status:** accepted

**Considered options:** symlink only (matches other hosts; broken on this host); copy one root only (risk silent miss); copy both roots (chosen).

**Consequences:** Copies drift until the installer is re-run after canonical plugin updates (see **copy freshness** in CONTEXT).
