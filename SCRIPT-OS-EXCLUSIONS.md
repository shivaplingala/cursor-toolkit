# Script OS exclusions

Which **shell** and **Python** scripts in this repo **cannot run** (or cannot run fully) on Linux, macOS, or Windows.

**Windows column means native `cmd.exe` / PowerShell.** Git Bash and WSL count as Unix shells (same as Linux for these scripts).

Legend: **run** = intended to work · **no** = do not run · **partial** = runs only with extra tools / notes.

### Writing new scripts

- **Python:** detect OS (`sys.platform` / `platform.system()`) and use that OS’s launcher and commands (`py -3` on Windows native; `python3` on Unix/WSL; no hardcoded Unix-only shells).
- **Shell:** write OS-specific files — `.sh` for Linux/macOS/Git Bash/WSL (bash 3.2-safe); `.ps1` for Windows native. Do not use `.sh` on `cmd.exe` / PowerShell.

---

## Shared: all `.sh` files

| OS | Exclusion |
|----|-----------|
| Linux | None (bash required). |
| macOS | None (bash required; macOS 10.15+ still has bash 3.2 — these scripts avoid bash-4-only syntax). |
| Windows native | **All `.sh` files** — no bash. Use **Git Bash** or **WSL**. |

---

## Shell scripts

| Script | Linux | macOS | Windows native | Extra exclusions |
|--------|:-----:|:-----:|:--------------:|------------------|
| `install.sh` | run | run | **no** | Git Bash/WSL: run. Symlinks may fail → files are copied. |
| `scripts/deps.sh` | run | run | **no** | **Linux:** apt only if `apt-get` exists. **macOS:** brew packages only if Homebrew exists; otherwise skip + message. **Windows Git Bash:** no apt/brew; prints **winget** hints only (does not install via winget from bash). |
| `plugins/full-cycle-delivery/scripts/install-multi-agent.sh` | run | run | **no** | Uses `host-discovery.sh`. |
| `plugins/full-cycle-delivery/scripts/lib/host-discovery.sh` | run | run | **no** | Sourced, not executed alone. **Windows Git Bash:** `ln -s` often fails → **copy** instead of symlink. |
| `plugins/full-cycle-delivery/scripts/fcd-doctor.sh` | run | run | **no** | |
| `plugins/full-cycle-delivery/scripts/test-host-matrix.sh` | run | run | **no** | Needs plugin dirs under `HOME`; `mktemp` + bash. |
| `plugins/fcd-v2/scripts/install-symlinks.sh` | run | run | **no** | Same symlink→copy fallback. |
| `plugins/global-tooling/scripts/install-multi-agent.sh` | run | run | **no** | |
| `plugins/aws-diagnose/skills/aws-diagnose-read/scripts/diag_epoch.sh` | run | **partial** | **no** | **macOS:** stock `date` has no `-d`. **Excluded unless** `gdate` (coreutils) or `DATE_CMD` pointing at GNU date. Duplicate: `skills/aws-diagnose-read/scripts/diag_epoch.sh`. |
| `skills/git-guardrails-claude-code/scripts/block-dangerous-git.sh` | run | run | **no** | Needs **jq**. Claude Code PreToolUse hook, not a user CLI. |
| `skills/diagnose/scripts/hitl-loop.template.sh` | run | run | **no** | Template; interactive `read`. Copy and edit before use. |

---

## Python scripts

Need **Python 3**. On Windows native, `python3` is often missing — use `py -3` or install Python and add it to PATH.

| Script | Linux | macOS | Windows native | Extra exclusions |
|--------|:-----:|:-----:|:--------------:|------------------|
| `plugins/aws-diagnose/skills/aws-diagnose-read/scripts/aws_read.py` | run | run | **run** if `python`/`py -3` | Needs **AWS CLI** + credentials. Duplicate: `skills/aws-diagnose-read/scripts/aws_read.py`. |
| `plugins/aws-diagnose/skills/aws-diagnose-read/scripts/scan_sst.py` | run | run | **run** if Python 3 | Walks the filesystem; no OS lock. |
| `skills/aha-video-understanding/scripts/aha_creds.py` | run | run | **run** if Python 3 | Library-style helper; imported by the others. |
| `skills/aha-video-understanding/scripts/aha_comments.py` | run | run | **run** if Python 3 | Needs Aha token (`AHA_API_TOKEN` or `~/.cursor/mcp.json`). |
| `skills/aha-video-understanding/scripts/aha_list_comments.py` | run | run | **run** if Python 3 | Same. |
| `skills/aha-video-understanding/scripts/aha_list_comment_videos.py` | run | run | **run** if Python 3 | Same. |
| `skills/aha-video-understanding/scripts/aha_list_comment_images.py` | run | run | **run** if Python 3 | Same. |
| `skills/aha-video-understanding/scripts/aha_download_video.py` | run | run | **run** if Python 3 | Writes to `~/.cache/aha-videos/` (`Path.home()`). |
| `skills/aha-video-understanding/scripts/aha_download_images.py` | run | run | **run** if Python 3 | Writes to `~/.cache/aha-images/`. |

---

## Quick “do not run” lists

### Do not run on Windows (`cmd` / PowerShell)

Every file ending in `.sh` listed above.

Python: none are excluded if Python 3 is on PATH (`py -3` on Windows). Aha helpers still need an Aha token.

### Do not run on macOS (stock install)

- `diag_epoch.sh` — **excluded** until GNU `date` / `gdate` is installed.

### Do not run on Linux

None of these scripts are Linux-excluded. `deps.sh` skips apt on distros without `apt-get` (Fedora, Alpine, etc.) — package install is excluded there; pip/npm parts still run.

---

## Not in this file

Node `.mjs` under `skills/codebase-doc-*` are not shell/Python. Run with Node on any OS that has Node.
