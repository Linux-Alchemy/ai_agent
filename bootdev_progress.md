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

- **Tool functions:** `functions/<name>.py` at repo root (not under `src/`).
- **Test modules:** print-based, at repo root, named `test_<name>.py`.
- **Main app:** `src/ai_agent/main.py` (ch1 OpenRouter chatbot).
- **Config:** `config.py` at repo root (`MAX_CHARS = 10000`).
- **Path-validation pattern** (reused by every tool function):
  ```python
  working_dir_abs = os.path.abspath(working_directory)
  target = os.path.normpath(os.path.join(working_dir_abs, path))
  valid = os.path.commonpath([working_dir_abs, target]) == working_dir_abs
  ```
- **Env:** uv (`uv add`, never bare pip; pip-safety skill applies), basedpyright
  on recommended (full type hints mandatory), ruff line-length 88, pytest.
- **Run a test module:** `uv run python test_<name>.py`.

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

### Next up
- **ch2/L6** — expected: `run_python_file` (execute a python file in the sandbox).
- After that: register the functions as tool schemas and build the agent loop
  (function calling) — that's the back half of ch2 / ch3.

### Open items
- Fixed docstrings added to `get_files_info` and `write_file` (Google style).
- Watch for a stray `calulator/` dir from a typo'd test arg (see if it lingers).
