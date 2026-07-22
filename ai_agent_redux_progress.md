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
| | 1.3 centralise path resolution + close symlink escape | not started |
| **2** Control | 2.1 approval gate | not started |
| | 2.2 `edit_file` tool + diff | **CUT — removed from scope** |
| **3** Execution isolation | 3.2 Bubblewrap process boundary | not started |
| **4** Polish | 4.1 Rich terminal interface | not started |
| | 4.2 final report + JSONL audit log | **CUT — removed from scope** |
| | 4.3 README as changelog | not started |
| **Optional** Security showcase | 3.1 prompt-injection demo + mitigation | deferred until after Phase 4 |
| **Housekeeping** | remove retired cut-feature stubs | ✅ done |

**Retired Phase 0 artifacts removed:** `src/ai_agent/functions/edit_file.py`,
`src/ai_agent/report.py`, and `tests/test_edit_file.py` were deleted during the
2026-07-22 housekeeping pass. `tests/test_injection.py` remains as the optional
task's stub.

---

## ▶ Resume here

**Next: Task 1.3** — fill `resolve_in_workdir` in `sandbox.py` (stub + full
contract docstring already in place), swap the four tools' inline containment
blocks for it, then write the symlink-escape test (1.3.4 — the first adversarial
test). Mode not yet chosen. Pair session via Obie-Wan.

---

## Change log (newest first)

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
- `tests/test_injection.py` — 2 tests (deferred with optional Task 3.1.4)

**Verification:**
- `uv run python -c "import ai_agent.sandbox, ai_agent.approval, ai_agent.report, ai_agent.functions.edit_file"` → all four import OK.
- `uv run python -m pytest tests/test_sandbox.py tests/test_edit_file.py tests/test_injection.py -v` → 8 skipped.

**Known noise (accepted at the time):** active stubs show unused-import /
unfilled-body warnings until their blocks are filled. The cut-feature stubs were
removed in the 2026-07-22 housekeeping pass.
