# ai_agent v2 — Build Plan

> **Companion to:** `OUTLINE.md` (read that first for the what/why)
> **This file is:** the how — every task, in order, addressable down to the block.

**How to use this file:** work top to bottom, one block at a time. Check boxes
as you go. Do not cross a Phase Checkpoint until it passes. Blocks are addressed
as Phase.Task.Block (e.g. 2.1.3) — that address is how work gets discussed,
delegated, and reported.

**This is a learning continuation.** The boot.dev course built the engine; this
plan extends the same concepts deeper, tutor-style, toward a display-ready
portfolio piece. Default posture: read the skeleton, understand the concept
named in the pseudocode, write the body yourself. Delegate a block only when
you've decided it's not the one worth typing by hand.

**Scope note (2026-07-24):** `OUTLINE.md` and this plan define the reduced core
build: sandbox path hardening, the approval gate, and Rich output. The
prompt-injection showcase is optional and appears after the core phases.
OS-level process isolation is recorded as a possible future upgrade.

**Two standing constraints, every block:**
- **Lean.** No unnecessary code, no speculative abstraction. If a block can be
  five clean lines, it is not eight clever ones.
- **Honest.** Test code stays at genuine beginner level — plain functions,
  simple asserts, `tmp_path`. Nothing here should imply mastery you're still
  building toward. Holes are fine and get documented, not hidden.

---

## Agent Delegation Protocol

When handed a block reference (e.g. "do 2.1.3"):
1. Read the relevant Phase header and Task header first. Then execute ONLY the
   named block(s).
2. Respect the task's Don't Touch list. No wandering, no opportunistic
   refactoring.
3. Ask first before: adding or upgrading any dependency, changing any function
   signature defined in a Skeleton, modifying files outside the named task, or
   touching anything schema- or config-shaped.
4. Never: commit secrets, delete or skip a failing test, edit vendored code,
   or add abstraction the block didn't ask for.
5. Report completion with evidence: the command you ran and its actual output.
   "Done ✓" is not evidence.
6. If a block is blocked (missing prerequisite, ambiguity), report it by
   address and stop. Don't improvise around it.

---

## Project Map

```
ai_agent/
├── src/ai_agent/
│   ├── main.py               # agent loop; --auto-approve originates here
│   ├── call_functions.py     # THE choke point — dispatch, wd injection, and approval gate
│   ├── config.py             # MAX_CHARS; gains WORKING_DIR constant (P1)
│   ├── prompts.py            # system prompt; optional injection-defence framing
│   ├── sandbox.py            # NEW (P1) — one resolve_in_workdir() helper, shared by all tools
│   ├── approval.py           # NEW (P2) — confirm() gate, --auto-approve aware
│   └── functions/
│       ├── get_files_info.py     # uses sandbox helper (P1)
│       ├── get_file_content.py   # uses sandbox helper (P1)
│       ├── write_file.py         # uses sandbox helper (P1) + gated (P2)
│       └── run_python_file.py    # uses sandbox helper (P1) + gated (P2)
├── tests/                    # print-scripts → pytest (P1)
│   ├── test_sandbox.py       # NEW (P1) — includes the symlink-escape attack test
│   └── test_injection.py     # OPTIONAL — mitigation wiring regression test
└── README.md                 # limitations list → concise hardening changelog
```

**Dispatch flow (the choke point that makes this plan lean):**
```
model → main.py loop → call_function()
                          ├─ resolve working_directory   (P1: WORKING_DIR)
                          ├─ approval gate                (P2: confirm before dangerous tools)
                          └─ dispatch to tool fn
```

---

## Phase 1: Build the Safety Net

**Phase goal:** Real tests exist, and direct tool paths cannot escape the
working-directory boundary, including through symlinks. Nothing below this phase
gets refactored without a net.
**Time estimate:** ~2.5–3.5 hours
**Files created / modified:** `sandbox.py` (new), `config.py`, all four
`functions/*.py`, `call_functions.py`, `tests/` (rewritten), `test_sandbox.py`
(new)
**Phase constraint:** No new features, no new tools. This phase only *proves and
protects* what already exists. Behaviour of the four tools stays identical apart
from symlink rejection.

---

### Task 1.1: Migrate the print-scripts to pytest

**File:** `tests/test_get_files_info.py`, `tests/test_get_file_content.py`,
`tests/test_write_file.py`, `tests/test_run_python_file.py`

The current test files are `print(...)` scripts you eyeball. Convert them to
pytest functions with real assertions. This is deliberately kept **beginner
level** — the goal is to show you know what pytest *is* and can drive it, not to
demonstrate fixture wizardry.

**Skeleton (pattern for each file):**
```python
from ai_agent.functions.write_file import write_file


def test_write_file_reports_char_count(tmp_path):
    """A successful write returns the success message with the char count."""
    ...


def test_write_file_rejects_escape(tmp_path):
    """A path outside the working directory returns an Error string."""
    ...
```

**What it does:**
1. For each existing print-script, turn each `print(fn(...))` line into a test
   function that calls the same function and `assert`s on the return string
   (`"Success" in result`, `result.startswith("Error:")`, etc.).
2. Use `tmp_path` as the working directory instead of the real `calculator/`
   dir. → *`tmp_path` is pytest's built-in per-test temp directory fixture — each
   test gets a fresh empty dir, so tests don't tread on each other or on real
   files.*
3. Keep assertions loose and readable — substring checks are fine. Don't assert
   exact full strings that'll break on a wording tweak.
4. One behaviour per test function. Two or three tests per file is plenty.

**Imports needed:** the function under test; `pytest` only if you use `tmp_path`
type hints (you don't need to).

**Rules:** Beginner-level only — no `parametrize`, no mocking, no fixtures beyond
`tmp_path`. If a test needs more than ~6 lines, it's trying too hard.

**Don't touch:** the `functions/*.py` implementations themselves — this task only
tests them. The `calculator/` directory.

**Blocks:**
- [x] **1.1.1** — Rewrite `test_write_file.py` as pytest functions using `tmp_path`.
- [x] **1.1.2** — Rewrite `test_get_files_info.py` and `test_get_file_content.py` the same way.
- [x] **1.1.3** — Rewrite `test_run_python_file.py` the same way.
- [x] **1.1.4** — Verify: `uv run python -m pytest -v` → all tests collected and passing.

_Completed before the 2026-07-22 rescope; recorded from the progress log._

---

### Task 1.2: Extract the sandbox root to config

**File:** `config.py`, `call_functions.py`

Right now `working_directory` is the string literal `"./calculator"` buried at
line 67 of `call_functions.py`. Lift it to a resolved constant.

**Skeleton (`config.py` addition):**
```python
import os

WORKING_DIR: str = os.path.realpath("./calculator")
```

**What it does:**
1. Add `WORKING_DIR` to `config.py`, resolved once at import with
   `os.path.realpath`. → *`realpath` collapses symlinks and `..` to a single
   canonical absolute path — the fixed reference point every containment check
   compares against.*
2. In `call_functions.py`, replace the `"./calculator"` literal with
   `WORKING_DIR` imported from config.
3. That's it. Do not add existence-checking or error-raising here yet — keep the
   change surgical.

**Imports needed:** `from ai_agent.config import WORKING_DIR` in `call_functions.py`.

**Rules:** One constant, one import swap. Resist the urge to "improve" config
while you're in there.

**Don't touch:** the tool functions; `main.py`.

**Blocks:**
- [x] **1.2.1** — Add resolved `WORKING_DIR` to `config.py`.
- [x] **1.2.2** — Swap the literal in `call_functions.py` for the imported constant.
- [x] **1.2.3** — Verify: `uv run python -m ai_agent.main "list the files"` → runs and lists `calculator/` contents as before.

_Completed before the 2026-07-22 rescope; recorded from the progress log._

---

### Task 1.3: Centralise path resolution and close symlink escapes

**File:** `sandbox.py` (new), then all four `functions/*.py`

Each tool currently repeats the same `abspath` / `normpath` / `commonpath`
containment dance. Two problems: it's duplicated four times (not lean), and
`normpath` does **not** resolve symlinks — a symlink inside the sandbox pointing
at `/etc/passwd` passes the check. Extract one helper that does it correctly,
once.

**Skeleton (`sandbox.py`):**
```python
import os


def resolve_in_workdir(working_directory: str, file_path: str) -> str | None:
    """Resolve file_path under working_directory, or None if it escapes.

    Joins file_path onto working_directory and fully resolves the result —
    following symlinks and collapsing ``..`` — then confirms it still sits
    inside working_directory. Returns the resolved absolute path on success,
    or None if the path escapes the sandbox (including via symlink).

    Args:
        working_directory: The sandbox root. Assumed already realpath-resolved.
        file_path: Untrusted path, relative to working_directory.

    Returns:
        The resolved absolute path if contained, otherwise None.
    """
    ...
```

**What it does:**
1. Join `working_directory` and `file_path`, then `os.path.realpath` the result.
   → *Doing `realpath` on the **final** joined path is the whole point:
   `normpath` (the current approach) resolves `..` textually but happily follows
   a malicious symlink out of the sandbox. `realpath` resolves the symlink
   too, so the containment check sees the real destination.*
2. Contain-check with `os.path.commonpath([working_directory, resolved]) ==
   working_directory` (same logic as today, now on the fully-resolved path).
3. Return the resolved path if contained, else `None`. Let each caller turn
   `None` into its own `Error:` message — the helper stays purpose-agnostic.
4. Update each of the four tool functions to call the helper and handle `None`,
   deleting their inline containment blocks.

**Imports needed:** `from ai_agent.sandbox import resolve_in_workdir` in each tool.

**Rules:** The helper returns a path or `None` — it does **not** print, raise, or
format error strings. Keep the "what went wrong" phrasing in the callers where it
already lives. One helper, four thin call sites.

**Don't touch:** the tools' schemas; their docstrings' *Returns* contracts still
hold, so leave them. `main.py`.

**Blocks:**
- [x] **1.3.1** — Write `resolve_in_workdir` in `sandbox.py` per the skeleton.
- [x] **1.3.2** — Replace the inline containment block in `write_file.py` and `run_python_file.py` with the helper.
- [x] **1.3.3** — Replace it in `get_file_content.py` and `get_files_info.py`.
- [x] **1.3.4** — Write `tests/test_sandbox.py`: one test for a normal contained path (returns a path), one for a `../` escape (returns `None`), and **one that creates a symlink via `tmp_path` pointing outside and asserts it's rejected**. → *That third test is your first adversarial test — you're attacking your own boundary and proving it holds.*
- [x] **1.3.5** — Verify: `uv run python -m pytest -v` → green, including the symlink-escape test.

---

### Phase 1 Checkpoint
- [x] `uv run python -m pytest -v` → 11 passed, 2 optional injection tests skipped.
- [x] A symlink pointing outside the sandbox is provably rejected (test exists and passes).
- [x] Path-containment logic lives in exactly one place.
- [ ] The agent still runs end-to-end: `uv run python -m ai_agent.main "fix the bug"` behaves as before.
- [x] **Committed:** implementation `71edba5`; sandbox tests and verification `93dbb5f`.

---

## Phase 2: Take Control of the Agent

**Phase goal:** Dangerous actions require human sign-off, with an explicit
`--auto-approve` escape hatch for trusted runs.
**Time estimate:** ~1.5–2 hours
**Files created / modified:** `approval.py` (new), `call_functions.py`, `main.py`,
and one approval test
**Phase constraint:** The approval gate is a *UX/control* layer, not process
isolation or a sandbox. Keep it that way.

---

### Task 2.1: The approval gate

**File:** `approval.py` (new), `call_functions.py`, `main.py`

Before `write_file` or `run_python_file` executes, ask the human. A
`--auto-approve` flag skips the prompt for when you trust the run. Because
`call_function` is the single dispatch point, the gate lives there — one check,
not one-per-tool.

**Skeleton (`approval.py`):**
```python
DANGEROUS: frozenset[str] = frozenset({"write_file", "run_python_file"})


def needs_approval(function_name: str, auto_approve: bool) -> bool:
    """Return True if this call must be confirmed by the human first.

    Args:
        function_name: The tool the model wants to run.
        auto_approve: If True, nothing is ever gated.

    Returns:
        True if the call is dangerous and auto_approve is off.
    """
    ...


def confirm(function_name: str, function_args: dict) -> bool:
    """Prompt the human to approve one tool call. Returns their yes/no.

    Prints the tool name and its arguments, then reads a y/N answer from
    stdin. Anything other than an explicit yes is treated as no.
    """
    ...
```

**What it does:**
1. `needs_approval`: pure predicate — `function_name in DANGEROUS and not
   auto_approve`. No I/O. → *Keeping the decision (pure) separate from the prompt
   (I/O) means you can unit-test the decision without simulating stdin.*
2. `confirm`: print the tool name + args, `input("Approve? [y/N] ")`, return
   `True` only on an explicit `y`/`yes`. Default-deny.
3. In `call_function`: after resolving the name, if `needs_approval(...)` and not
   `confirm(...)`, return a tool message with content like `"Error: user denied
   {name}"` — the model sees the denial as a normal tool result and can adapt.
4. Thread an `auto_approve: bool` param from `main.py`'s argparse
   (`--auto-approve`) down into `call_function`.

**Imports needed:** `from ai_agent.approval import needs_approval, confirm` in
`call_functions.py`.

**Rules:** Default-deny — any answer that isn't clearly yes means no. The gate
returns a normal tool message on denial (don't raise, don't exit — let the agent
loop keep going). Don't gate the read-only tools.

**Don't touch:** the tool functions themselves; the sandbox helper. Schemas.

**Blocks:**
- [x] **2.1.1** — Write `approval.py` (`DANGEROUS`, `needs_approval`, `confirm`) per the skeleton.
- [x] **2.1.2** — Add `--auto-approve` to argparse in `main.py` and thread it into `call_function`'s signature.
- [x] **2.1.3** — Insert the gate in `call_function` before dispatch; denial returns a tool message.
- [x] **2.1.4** — Add one pytest for `needs_approval` (dangerous+not-auto → True; read-only → False; auto → False). Leave `confirm` untested (it's stdin I/O — note that as a known, acceptable hole).
- [x] **2.1.5** — Verify: `uv run python -m ai_agent.main "write hello to test.txt"` prompts before writing; `--auto-approve` skips the prompt.

---

### Phase 2 Checkpoint
- [x] Writes and executions prompt for approval; `--auto-approve` bypasses.
- [x] Denial is handled gracefully (agent loop continues, model sees the denial).
- [x] `uv run python -m pytest -v` green.
- [x] **Commit:** `git commit -m "Phase 2: add approval gate"` (landed as `bef2592`)

---

## Phase 3: Polish

**Phase goal:** Give the agent a restrained Rich terminal interface and finish
the README.
**Time estimate:** ~1.5–2.5 hours
**Files created / modified:** `main.py`, `call_functions.py`, `README.md`,
`pyproject.toml` (add `rich`)
**Phase constraint:** Presentation and documentation only. No behaviour changes
to tools, sandbox, or gate. If you find yourself editing a tool's logic here,
stop — that's not this phase.

---

### Task 3.1: Rich terminal interface

**File:** `main.py`, `call_functions.py`, `pyproject.toml`

Replace the bare `print`s with Rich: a panel per tool call, a spinner while the
model thinks, colour for success/error, and a compact token footer. The approval
prompts and tool results are the useful content; the interface should stay quiet.

**What it does:**
1. Before `uv add rich`, read and follow the pip-safety protocol, then ask for
   dependency-change approval per the Agent Delegation Protocol.
2. In `main.py`: wrap the model call in a `console.status("thinking…")` spinner;
   print the final response in a `Panel`.
3. In `call_functions.py`: render each tool call as a compact line/panel
   (name + args), colour the result green on success / red on `Error:`.
4. Keep it restrained — this is a CLI agent, not a light show. A spinner, panels,
   two colours. → *Lean applies to visual design too: the goal is legible, not
   busy.*

**Imports needed:** `from rich.console import Console`, `from rich.panel import Panel`.

**Rules:** Presentation only — don't change what any tool returns, only how it's
displayed. Don't let Rich formatting leak into the strings sent back to the model
(the model wants plain text; Rich is for the human's terminal).

**Don't touch:** tool logic, sandbox, or approval. Any `.py` in `functions/`.

**Blocks:**
- [ ] **3.1.1** — Follow pip-safety, obtain approval, then `uv add rich`; create a shared `Console`.
- [ ] **3.1.2** — Add the thinking spinner and final-response panel in `main.py`.
- [ ] **3.1.3** — Colour and frame tool calls/results in `call_functions.py` (human-facing output only).
- [ ] **3.1.4** — Verify: `uv run python -m ai_agent.main "list files"` shows spinner + panelled output; model still receives plain-text results (spot-check with `--verbose`).

---

### Task 3.2: README as changelog

**File:** `README.md`

Turn the existing "Known limitations" section into the story of the build: what
was broken, what you did, what's still deliberately incomplete.

**What it does:**
1. Convert "Known limitations" into a concise changelog of the completed core
   phases — each phase's before/after in a couple of lines.
2. Keep the honest holes visible: `confirm` is untested, executed Python has no
   OS-level isolation, and prompt injection remains untreated unless the
   Optional section is completed. → *A visible limitations list shows that the
   boundary of the work is understood; it is not a confession booth.*
3. Add a one-line "how to run" up top.

**Rules:** Honest and lean. Don't dress up the holes; don't dwell on them either.

**Don't touch:** any code — this is docs only.

**Blocks:**
- [ ] **3.2.1** — Rewrite the README: run instructions, phase changelog, honest limitations.
- [ ] **3.2.2** — Verify: README renders on GitHub; every claim maps to something real in the repo.

---

### Phase 3 Checkpoint
- [ ] Output is Rich-formatted (spinner, panels, colour) — human-facing only.
- [ ] README tells the reduced-scope build story honestly, holes included.
- [ ] `uv run python -m pytest -v` green.
- [ ] **Commit:** `git commit -m "Phase 3: add Rich UI and polish README"`

---

## Optional Phase 4: Security Showcase

This section is outside the core completion path. Decide after Phase 3 whether
the portfolio value is worth the extra time. Skipping it does not leave any core
phase incomplete.

### Task 4.1: Prompt-injection demo and mitigation

**File:** `tests/test_injection.py` (new), `prompts.py`, `call_functions.py`,
`README.md`

Plant a hostile instruction inside a file the agent reads, show the agent obeying
it, then mitigate by framing tool results as untrusted data and pin the wiring as
a regression test.

**What it does:**
1. **Attack:** create a sandbox file containing a hostile instruction, run the
   agent against it, and record the observed behaviour. → *This is indirect
   prompt injection: instructions arrive disguised as data consumed by a tool.*
2. **Mitigate:** frame tool results as untrusted data in `call_functions.py` and
   tell the model in `prompts.py` that file contents and tool output are data,
   never commands. These are defence-in-depth measures, not a hard boundary.
3. **Regression test:** assert that the delimiter is applied to tool results and
   the defence instruction remains in the system prompt. This pins the wiring,
   not the model's behaviour.
4. **Document:** add attack, mitigation, and limitations to the README without
   claiming that prompt injection has been solved.

**Imports needed:** only existing project imports needed by the test.

**Rules:** No behavioural-evaluation framework. No new dependency. Describe the
mitigation as risk reduction, not prevention.

**Don't touch:** tool-function logic, the sandbox helper, approval behaviour, or
process-execution behaviour.

**Blocks:**
- [ ] **4.1.1** — Reproduce the attack manually; note the agent's behaviour for the README.
- [ ] **4.1.2** — Add the untrusted-data delimiter to tool results in `call_function`.
- [ ] **4.1.3** — Add the injection-defence line to the system prompt in `prompts.py`.
- [ ] **4.1.4** — Write `test_injection.py` asserting the mitigation is wired in.
- [ ] **4.1.5** — Write the README section: attack → mitigation → honest limitations.
- [ ] **4.1.6** — Verify: `uv run python -m pytest -v` green; README section reads clearly.

### Optional Phase 4 Checkpoint
- [ ] The attack is reproduced, mitigated, documented, and pinned by a wiring test.
- [ ] The README distinguishes prompt-level mitigation from hard sandbox controls.
- [ ] **Commit:** `git commit -m "Optional: document and mitigate prompt injection"`

---

## Possible Future Upgrade: OS-Level Process Isolation

`run_python_file` currently limits the target path and execution time, but the
child process is not isolated from the wider filesystem or network. Bubblewrap
(`bwrap`) is a possible future hardening upgrade once its Linux namespace and
bind-mount model is properly understood. If taken on, it should fail closed when
`bwrap` is unavailable and should be planned as a separate phase rather than
bolted casually onto the existing tool.

---

## Quick Reference: Don't Touch List

| Phase | Off-limits |
|---|---|
| 1 | Tool *features* (test & protect only); `calculator/`; schemas |
| 2 | Process isolation; read-only tools stay ungated |
| 3 | All tool/sandbox/gate *behaviour* — presentation and docs only |
| Optional 4 | Tool logic, sandbox, approval behaviour, and process execution |

---

## Change Log

- **2026-07-24** — Reduced the remaining core to sandbox path hardening, the
  approval gate, and Rich polish. Moved Bubblewrap process isolation to a
  possible future upgrade, renumbered the remaining work sequentially, and kept
  the prompt-injection showcase as Optional Phase 4.
- **2026-07-22** — Marked Tasks 1.1 and 1.2 complete from the existing progress
  log; the plan then resumed at Task 1.3.
