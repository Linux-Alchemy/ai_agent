# ai_agent v2 (Redux) — Progress Log

Tracks what has changed versus the original boot.dev **"project complete"**
baseline, so the final writeup is honest about what's ours versus what the
course produced. Companion to `OUTLINE.md` (what/why) and `PLAN.md` (how).

**Baseline reference:** commit `de92b4a` ("final commit, project complete") —
~200 lines, four tools, `print(...)` "tests" you eyeball, hardcoded
`./calculator` working dir, no approval gate, no process isolation.

---

## Status board

| Phase | Task | State |
|---|---|---|
| **0** Bench prep | new files stubbed | ✅ done |
| **1** Safety net | 1.1 print-scripts → pytest | ✅ done |
| | 1.2 extract `WORKING_DIR` to config | ✅ done |
| | 1.3 centralise path resolution + close symlink escape | ✅ done |
| **2** Control | 2.1 approval gate | ✅ done — all blocks; commit pending |
| **3** Polish | 3.1 Rich terminal interface | not started |
| | 3.2 README as changelog | not started |
| **Optional 4** Security showcase | 4.1 prompt-injection demo + mitigation | deferred until after Phase 3 |
| **Future** Process isolation | Bubblewrap boundary | possible later upgrade |
| **Housekeeping** | remove retired cut-feature stubs | ✅ done |

**Retired Phase 0 artifacts removed:** `src/ai_agent/functions/edit_file.py`,
`src/ai_agent/report.py`, and `tests/test_edit_file.py` were deleted during the
2026-07-22 housekeeping pass. `tests/test_injection.py` remains as the optional
task's stub.

---

## ▶ Resume here

**Next: Task 3.1 — Rich terminal interface.** Phase 2 is functionally complete;
the only outstanding item is its checkpoint commit
(`git commit -m "Phase 2: add approval gate"`).

Paired mode — Matt writes, Obie-Wan reviews.

---

## Change log (newest first)

### 2026-07-25 — Blocks 2.1.2–2.1.5: gate wired in; **Task 2.1 complete**

Paired (Matt writing, Obie-Wan reviewing). The gate is now live end to end.

- **2.1.2 — plumbing.** `--auto-approve` added to argparse in `main.py`
  ("Enable YOLO mode. Use at your own risk"); `auto_approve: bool = False` added
  to `call_function`'s signature and threaded through at the call site. The
  `False` default means a caller who forgets to pass it fails *closed*.
- **2.1.3 — the gate.** In `call_functions.py`, between the unknown-function
  guard and the `working_directory` injection:
  `if needs_approval(function_name, auto_approve) and not confirm(function_name,
  function_args): return {...}`. Denial returns a normal tool message —
  `f"Error: Action cancelled by user: {function_name}"` — matching the
  `Error:` register of the unknown-function return above it.
  Two placement decisions worth keeping: the pure predicate is the **left**
  operand so short-circuiting means `confirm`'s stdin prompt never fires for
  read-only tools; and the gate sits **before** `working_directory` is injected
  so the human sees exactly what the model asked for, not internal plumbing.
- **2.1.4 — tests.** `tests/test_approval.py`, three tests against
  `needs_approval` (dangerous+not-auto → True, read-only → False, auto → False),
  asserting with `is True` / `is False` rather than truthiness. `confirm` left
  untested by design, noted in-file.
- **2.1.5 — live verification.** `uv run main.py "write 'hello' to testfile.txt"
  --verbose` prompted before writing; a denial produced
  `-> Error: Action cancelled by user: write_file`, and the model adapted in the
  next turn ("I cannot write to `testfile.txt`. Is there another file I can
  write to?") rather than the loop falling over. That behaviour — denial as a
  normal tool result, not an exception — was the point of the design.

**Also this session:** module docstring added to `approval.py` (closes a hole
carried from the 2.1.1 entry below); the `--auto-apporve` typo caught in review
before it could produce a runtime `AttributeError`; ruff `line-length` widened
from 88 to 115 in `pyproject.toml` (Matt's call, noted rather than argued).

**Known, accepted holes (still carried):** `confirm`'s `EOFError` on
closed/piped stdin remains uncaught; `confirm` remains untested; `PLAN.md`'s
skeleton still types `function_args` as bare `dict`.

**Verification:** `uv run python -m pytest -v` → **14 passed, 2 skipped** in
0.20s. `uv run ruff check .` → All checks passed. The two skips remain the
deferred Optional Phase 4 injection tests.

### 2026-07-25 — Block 2.1.1: `approval.py` implemented

Paired (Matt writing, Obie-Wan reviewing). Both functions now land in one
expression each:

- `needs_approval` — pure predicate, `function_name in DANGEROUS and not
  auto_approve`. No I/O, so 2.1.4 can unit-test the decision without faking
  stdin.
- `confirm` — prints the pending tool name + args, reads `input("Approve
  [y/N]?: ")`, normalises with `.strip().lower()`, returns `response in {"y",
  "yes"}`. Default-deny: anything that isn't an explicit yes is a no.

The expanded step-by-step `# TODO 2.1.1` scaffolding was written into the file
first, then removed once both bodies were filled.

**Review findings raised and fixed by Matt during the session:**

1. **Inverted gate logic** — first draft read `... and auto_approve`, which would
   have prompted only when `--auto-approve` was on and written files silently on
   a normal run. Exactly backwards for a security gate.
2. **Retry loop broke default-deny** — an intermediate version looped on invalid
   input, so a bare Enter (`""`) retried forever instead of denying, contradicting
   both the `[y/N]` prompt and the docstring. Loop dropped in favour of the
   simple single-read version; a denial is cheap because the model just receives
   a tool message and adapts.
3. **Missing return on the deny path** — `return True` inside the `if` with
   nothing after it, so the function fell through to an implicit `None` and
   basedpyright flagged the `-> bool` contract. Collapsed to a direct expression
   return, matching `needs_approval`'s shape.

**Known, accepted holes (carried forward):**

- `input()` raises `EOFError` on closed/piped stdin; not currently caught, so a
  non-interactive run will traceback out of the gate rather than deny. Decision
  deferred, not overlooked.
- `confirm` stays untested by design (stdin I/O) — per plan block 2.1.4.
- `approval.py` still has no module docstring, unlike its siblings.
- `PLAN.md`'s skeleton types `function_args` as bare `dict`; the file uses
  `dict[str, object]`. The file is correct for basedpyright's recommended mode;
  the plan text has simply drifted.

**Verification:** `uv run python -m pytest -q` → **11 passed, 2 skipped** in
0.63s (unchanged — 2.1.1 adds no tests; that's 2.1.4). `uv run ruff check
src/ai_agent/approval.py` → All checks passed.

### 2026-07-24 — Task 1.3 complete; remaining plan renumbered

Implemented `resolve_in_workdir`, routed all four tools through it, and added
contained-path, `../` escape, and symlink-escape tests. The containment logic now
lives in one helper.

**Verification (1.3.5):** `uv run python -m pytest -v` → **11 passed, 2 skipped**
in 1.06s. The two skips are the deferred Optional Phase 4 injection tests.

Reduced the remaining core plan to Phase 2 control and Phase 3 polish, moved the
injection showcase to Optional Phase 4, and recorded Bubblewrap process
isolation as a possible future upgrade.

### 2026-07-22 — Reduced-scope housekeeping complete

Removed only the inert Phase 0 artifacts belonging to the two cut features:

- Deleted `src/ai_agent/functions/edit_file.py` (cut Task 2.2).
- Deleted `src/ai_agent/report.py` (cut Task 4.2).
- Deleted `tests/test_edit_file.py` (cut Task 2.2 test stub).
- Updated the README's targeted-edit limitation to state that whole-file writes
  are an accepted boundary of the reduced scope.

Preserved all in-scope work, including `sandbox.py`, `approval.py`, the four
existing tools and migrated tests, and optional `tests/test_injection.py`.
Reference audit found no dangling production imports or cut-task TODOs.

**Verification:** `uv run python -m pytest -v` → **8 passed, 5 skipped** in
0.26s. The skips are exactly the three Task 1.3 sandbox stubs and two optional
Task 3.1 injection stubs.

The active resume point remains **Task 1.3**.

### 2026-07-22 — Project rescope: five core upgrades + one optional

Reduced the remaining build to fit the available time while preserving the
security-hardening work already underway:

- **Kept:** pytest migration, symlink-safe sandboxing, approval gate,
  Bubblewrap execution isolation, Rich terminal output, and final README polish.
- **Cut:** Task 2.2 (`edit_file`) and Task 4.2 (run report + JSONL audit).
- **Deferred:** Task 3.1 (prompt-injection demo + mitigation) moved after Phase 4
  under **Optional**. Skipping it does not block core completion.
- **Documents updated:** `OUTLINE.md` now defines the reduced scope; `PLAN.md`
  preserves the cut task addresses, updates phase checkpoints and estimates, and
  moves the showcase to the end.
- **Repository reality at rescope:** the Phase 0 stubs for both cut features
  still existed as inert prep artifacts; they were removed in the housekeeping
  entry above.

The active resume point remains **Task 1.3**.

### 2026-07-21 — Task 1.2: extract WORKING_DIR to config

Solo (Matt). Added `WORKING_DIR: str = os.path.realpath("./calculator")` to
`config.py`; swapped the hardcoded `"./calculator"` literal at
`call_functions.py:69` for the imported constant. `realpath` now resolves the
sandbox root to a single canonical absolute path (the reference point Phase 1.3
containment checks will compare against). Only the intended literal remains, in
`config.py`.

**Verification (1.2.3):** `uv run python -m ai_agent.main "list the files…"` →
agent calls `get_files_info` and lists `calculator/` contents as before.

### 2026-07-21 — Blocks 1.1.3 + 1.1.4: run_python_file → pytest; Task 1.1 done

Paired. Rewrote `test_run_python_file.py`:
- `test_run_python_file_captures_output` — writes a tiny script, runs it, asserts
  its STDOUT is in the result (real subprocess).
- `test_run_python_file_rejects_non_python` — a `.txt` file returns `Error:`.

**Task 1.1 complete** — all four print-scripts are now real pytest.

**Verification (1.1.4):** `uv run python -m pytest -v` → **8 passed, 8 skipped**
(8 migrated tests green; the 8 forward-stubs report skipped, not false-passes).

### 2026-07-21 — Block 1.1.2: get_files_info + get_file_content → pytest

Paired. Rewrote both from print-scripts to two pytest functions each, using
`tmp_path` (annotated `tmp_path: Path`):
- `test_get_files_info.py` — lists contents (creates a file first, asserts name +
  `is_dir` format); rejects `"../"` escape.
- `test_get_file_content.py` — returns file contents (substring check); rejects
  `"../"` escape.

Old print-scripts removed (get_files_info) / commented for reference (get_file_content).
Optional truncation test for get_file_content noted but not taken — 2 tests suffices.

**Verification:** each file `uv run python -m pytest <file> -v` → 2 passed.

### 2026-07-21 — Block 1.1.1: test_write_file.py → pytest

Paired. Rewrote `tests/test_write_file.py` from print-scripts to two pytest
functions using `tmp_path`:
- `test_write_file_reports_char_count` — asserts `"Success"` in result (and the
  char count reflects the content length; input-verifies-output).
- `test_write_file_rejects_escape` — a `/tmp/...` path returns an `Error:` string.

Old print-scripts left commented in-file for reference (Matt tidying next).

**Verification:** `uv run python -m pytest tests/test_write_file.py -v` → 2 passed.

### 2026-07-21 — Phase 0: bench prep

Prepared the workbench ahead of Task 1.1. **No existing files removed**
(tidy-as-we-go: old files stay until their replacement is proven).

**New source stubs** (signature + contract docstring + `# TODO <block>` marker,
`...` bodies — import cleanly, do nothing yet):
- `src/ai_agent/sandbox.py` — `resolve_in_workdir` (fills at 1.3.1)
- `src/ai_agent/approval.py` — `DANGEROUS`, `needs_approval`, `confirm` (fills at 2.1.1)
- `src/ai_agent/functions/edit_file.py` — `edit_file`; schema left as a TODO
  comment (Task 2.2 later cut; stub removed 2026-07-22)
- `src/ai_agent/report.py` — `RunReport` dataclass (Task 4.2 later cut; stub
  removed 2026-07-22)

**New test stubs** (named functions with `pytest.skip("stub …")` bodies, so
they report **SKIPPED**, never a false pass):
- `tests/test_sandbox.py` — 3 tests (fills at 1.3.4)
- `tests/test_edit_file.py` — 3 tests (Task 2.2 later cut; stub removed 2026-07-22)
- `tests/test_injection.py` — 2 tests (now deferred with Optional Task 4.1.4)

**Verification:**
- `uv run python -c "import ai_agent.sandbox, ai_agent.approval, ai_agent.report, ai_agent.functions.edit_file"` → all four import OK.
- `uv run python -m pytest tests/test_sandbox.py tests/test_edit_file.py tests/test_injection.py -v` → 8 skipped.

**Known noise (accepted at the time):** active stubs show unused-import /
unfilled-body warnings until their blocks are filled. The cut-feature stubs were
removed in the 2026-07-22 housekeeping pass.
