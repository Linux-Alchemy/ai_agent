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
- **Main app:** `src/ai_agent/main.py` — holds `main()`. A three-line launcher at
  repo root (`main.py`) imports and calls it, so `uv run main.py` works from root.
  **This matters:** `bootdev run <hash>` executes from your cwd and invokes
  `uv run main.py`, while the agent's sandbox is the *relative* path
  `./calculator`. Both only resolve correctly from the repo root. Always run —
  and always paste the grader hash — from the repo root.
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
- **ch3/L2 (2026-07-11)** — function declaration / tool schemas. Added
  `schema_get_files_info` at the bottom of `functions/get_files_info.py`
  (typed `ChatCompletionToolParam`, imported from `openai.types.chat`). New
  `src/ai_agent/call_functions.py` assembles `available_functions:
  list[ChatCompletionToolParam]`. `main.py`: passes `tools=available_functions`
  to `create`; grabs `message = response.choices[0].message`; if
  `message.tool_calls`, loops and prints `Calling function: name(args)`, else
  prints `message.content`. Needed a `tool_call.type == "function"` guard to
  narrow the union (custom vs function tool calls) before touching `.function`.
  `json.loads(... or "{}")` parses the arg string. System prompt updated to list
  the available op. Test passed. Not calling functions yet — just printing intent.

- **ch3/L3 (2026-07-11)** — "More Declarations". Added the remaining three tool
  schemas at the bottom of their function files: `schema_get_file_content`,
  `schema_write_file` (two required props: `file_path` + `content`),
  `schema_run_python_file` (nested `args` array — `"type": "array"`,
  `"items": {"type": "string"}` — optional, so *not* in `required`). Wired all
  four into `available_functions` in `call_functions.py`. Updated the system
  prompt in `prompts.py` to list all four operations (exact grader wording).
  Still just *choosing* functions, not calling them yet. All four grader prompts
  passed.
  - **Model swap (root cause of a failing grader step):** `main.py` was on
    `model="openrouter/free"` — an auto-router that lands on weak free models
    that pick the wrong tool (`get_files_info` for "run main.py") and mangle args
    (`'pkg>'`). Switched to **Gemini 2.5 Flash** (`temperature=0` back in place) —
    deterministic, correct tool selection across all four prompts. The schemas
    were correct all along; the model was the problem.
  - **JSON schema lesson:** a trailing comma after the closing `}` of a dict
    literal turns it into a one-element tuple, which `ruff format` then wraps in
    parens — the source of the mysterious `= ( {...} )` in two files. Harmless
    once the comma's gone (parenthesised dict); worth spotting.

- **ch3/L4 (2026-07-12)** — "Calling Functions". The agent now actually *runs* the
  tool it picks. `call_function(tool_call, verbose)` added to `call_functions.py`:
  parses the JSON arg string, prints the call, dispatches via a
  `function_map: dict[str, Callable[..., str]]`, injects
  `function_args["working_directory"] = "./calculator"`, and returns a **tool
  message** (`role` / `tool_call_id` / `content`). `main.py` calls it in place of
  the old print, raises on empty content, and prints `-> {content}` when verbose.
  All four tools verified working end-to-end (list, read, write, run tests.py).
  **Grader passed.**
  - **Typing:** took the SDK's real types over the lesson's loose ones —
    `tool_call: ChatCompletionMessageFunctionToolCall` (the `.type == "function"`
    guard in `main.py` is what narrows the union to it) and
    `-> ChatCompletionToolMessageParam` (a TypedDict, so the three message keys are
    checked at edit time). `function_args: dict[str, Any]` — `json.loads` returns
    `Any`; that annotation marks the trust boundary honestly.
  - **`Callable[..., str]`:** the `...` deliberately skips parameter checking (the
    four functions have four different signatures); the `str` is the one guarantee
    they share, and it's what makes `"content": result` type-check.
  - **Gotcha — "unreachable code":** `if not result_message:` is dead code. A
    TypedDict with required keys can never be empty, so it's always truthy. Test
    the thing that *can* be empty: `if not result_message["content"]:`.
  - **Entry-point fix (see Project Conventions):** L2/L3 passed while being run
    from `src/ai_agent/`, because those lessons only *printed* the intended call —
    `working_directory` was never used, so cwd didn't matter. L4 is the first
    lesson that actually executes, so cwd started mattering and the two
    requirements collided. Fixed with `main()` + root launcher rather than
    flattening the src-layout.

### Next up
- **ch3/L5** — 3 lessons left in the course. Presumably: append the tool message to
  `messages` and send it back so the model can *use* the result (the lesson closed
  with "we aren't passing the function call results back to the LLM just yet"),
  then loop until the model stops asking for tools.

### Open items
- ~~**`temperature=0` removed from `main.py`'s `create` call** during ch3/L2~~ —
  resolved: restored during ch3/L3 alongside the Gemini 2.5 Flash swap. The
  grader wanted deterministic tool selection; it's back and staying.
- **Deliberately-left basedpyright note** in `main.py`: `function_args` reads as
  `Any` because `json.loads` returns `Any`. Harmless (only printed). A
  `cast(dict[str, object], ...)` at the parse boundary silences it if ever wanted.
- Fixed docstrings added to `get_files_info` and `write_file` (Google style).
- ~~Watch for a stray `calulator/` dir from a typo'd test arg~~ — resolved:
  removed the dir, Matt fixed the `"calulator"` typo in `test_write_file.py:4`.
- **Hardening — the sandbox root is relative and hardcoded.** `call_function` sets
  `working_directory` to the *relative* `"./calculator"`, so the agent's sandbox
  silently relocates depending on where you launch from. Proved it: running from
  `src/ai_agent/` made `write_file` `makedirs` a brand-new phantom
  `src/ai_agent/calculator/` and drop the file in there. The path validation was
  never at fault — it correctly guarded the boundary it was *given*. **A sandbox is
  only as good as the thing that defines its boundary.** Grown-up fix (post-course):
  resolve the sandbox root to an absolute path once at startup, fail loudly if it
  doesn't already exist, and stop `write_file` conjuring directories into being.
  Belongs in `config.py` next to `MAX_CHARS`.
- **Hardening (later polish pass):** `run_python_file` uses the literal
  `"python"` in the command list to satisfy the boot.dev grader. For real-world
  robustness, swap to `sys.executable` (the exact interpreter running the
  process) — `"python"` may be missing or point at Python 2 on some systems.
  Noted alongside the security warning now in `README.md`.
