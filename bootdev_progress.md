# boot.dev "Build an AI Agent" — Obie-Wan Working File

This is the memory file for the boot.dev AI-agent project. When Matt says we're
working on the boot dev project (with the `obie-wan` skill active), read this
first to pick up where we left off.

---

## Working Agreement

- **Ask for the lesson text first.** When Matt says we're starting a boot.dev
  lesson, ask him to paste the assignment text before doing anything. Don't work
  from memory of the course — work from what he pastes.
- **"Skeleton" means:** write into the required file — function signature(s) with
  full type hints, a Google-style contract-grade docstring, and **numbered TODO
  comments** derived from the lesson's pseudocode. Matt fills the bodies. Nothing
  more than what's named.
- **Coaching mode.** Matt is finding his Python legs after a break — be explicit,
  give step-by-step pseudocode, push him along. He writes the code; Obie-Wan
  flags and locates bugs (No Silent Fixes), he does the fixing.
- **Error strings are checked character-for-character** by the boot.dev grader.
  Match them exactly, punctuation and all.

## Project Conventions (this repo differs from the boot.dev default layout)

- **Tool functions:** `src/ai_agent/functions/<name>.py` (inside the package).
  Import as `from ai_agent.functions.<name> import <name>`.
- **Test modules:** print-based, in `tests/`, named `test_<name>.py`. Run them
  **from repo root** (they use relative working dirs like `"calculator"`).
- **Main app:** `src/ai_agent/main.py` (ch1 OpenRouter chatbot).
- **Config:** `src/ai_agent/config.py` (`MAX_CHARS = 10000`). Import as
  `from ai_agent.config import MAX_CHARS`.
- **Path-validation pattern** (reused by every tool function):
  ```python
  working_dir_abs = os.path.abspath(working_directory)
  target = os.path.normpath(os.path.join(working_dir_abs, path))
  valid = os.path.commonpath([working_dir_abs, target]) == working_dir_abs
  ```
- **Env:** uv (`uv add`, never bare pip; pip-safety skill applies), basedpyright
  on recommended (full type hints mandatory), ruff line-length 88, pytest.
- **Run a test module:** `uv run python tests/test_<name>.py` (from repo root).

---

## Progress Log

### Done
- **ch1** — `main.py` CLI chatbot via OpenRouter (`src/ai_agent/main.py`).
- **ch2/L3** — `get_files_info` (`functions/get_files_info.py`).
- **ch2/L4** — `get_file_content` (`functions/get_file_content.py`); added
  `config.py` (`MAX_CHARS`), `calculator/lorem.txt` (~20.5k chars),
  `test_get_file_content.py`. Reads up to MAX_CHARS, appends truncation notice.
- **ch2/L5** — `write_file` (`functions/write_file.py`); `test_write_file.py`.
  makedirs parents, overwrite in "w" mode, success string with char count.
- **ch2/L6** — `run_python_file` (`functions/run_python_file.py`);
  `test_run_python_file.py`. subprocess.run with `cwd`, `capture_output`,
  `text=True`, `timeout=30`; output built as list-of-parts, `"\n".join`ed.
  Added the security warning to `README.md`.
- **ch3/L1** — system prompt wired in: `src/ai_agent/prompts.py` holds
  `system_prompt`, imported into `main.py` and placed first in the `messages`
  list (system role). Needed `temperature=0` on the `create` call for
  deterministic output (the grader expects the exact response).

- **Housekeeping (2026-07-11)** — consolidated to a single src-layout root.
  Moved `config.py`, `functions/` → `src/ai_agent/`; moved root `test_*.py` →
  `tests/`; added `src/ai_agent/functions/__init__.py`; updated all imports to
  `ai_agent.*`; removed duplicate `.env` line in `.gitignore`. `git mv` used so
  history survives. Not yet committed.

### Next up
- **ch3/L2** — Matt picks this up next session (~2026-07-10).
- After that: register the functions as tool schemas and build the agent loop
  (function calling).

### Open items
- Fixed docstrings added to `get_files_info` and `write_file` (Google style).
- ~~Watch for a stray `calulator/` dir from a typo'd test arg~~ — resolved:
  removed the dir, Matt fixed the `"calulator"` typo in `test_write_file.py:4`.
- **Hardening (later polish pass):** `run_python_file` uses the literal
  `"python"` in the command list to satisfy the boot.dev grader. For real-world
  robustness, swap to `sys.executable` (the exact interpreter running the
  process) — `"python"` may be missing or point at Python 2 on some systems.
  Noted alongside the security warning now in `README.md`.
