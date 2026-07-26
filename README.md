# AI Agent

A small command-line coding agent built in Python. Give it a task and it can
inspect a working directory, read and write files, run Python, feed the results
back to an LLM, and keep going until it has an answer or reaches its 20-turn
limit. The memory is just a growing message history; the apparent magic is a
loop, four tools, and a model making increasingly consequential decisions.

This project began as the capstone for boot.dev's *Build an AI Agent* course.
The course supplied the original agent loop and tool set; this version keeps
that foundation and extends it with stronger path handling, automated tests,
human approval for dangerous actions, and a cleaner terminal interface.

## Security Warning

**This is a learning project, not a safe or production-ready agent.** It can
overwrite files and execute model-directed Python with the permissions of the
user running it. Do not point it at sensitive data, important code, or an
environment containing secrets you cannot afford to lose.

The filesystem checks and approval prompt reduce a few obvious risks, but they
do not make arbitrary code execution safe. In particular, the Python subprocess
has no OS-level filesystem or network isolation. A script launched from inside
the working directory can still reach beyond it. More on that under
[Known Limitations](#known-limitations), where the cupboard contains rather more
than one skeleton.

## Changes From The Course Version

The original course project was roughly 200 lines with four tools, a hardcoded
working directory, print-based checks that had to be inspected by eye, and no
approval step before writes or execution. This version adds:

1. **A real pytest suite.** The original print-and-inspect scripts were replaced
   with plain pytest tests covering all four tools, path containment, symlink
   escapes, and the pure approval-decision logic. The current suite has 14
   passing tests; two optional prompt-injection tests remain deliberately
   skipped. The interactive approval prompt itself is not tested.
2. **One resolved working-directory root.** `WORKING_DIR` is resolved to a
   canonical absolute path in configuration instead of being injected as a
   repeated `"./calculator"` literal.
3. **Centralised, symlink-aware path handling.** Every tool now goes through one
   `resolve_in_workdir()` helper. It resolves `..` components and symlinks before
   checking containment, closing the original symlink-escape hole.
4. **Human approval for dangerous tools.** `write_file` and `run_python_file`
   require an explicit `y` or `yes`. Anything else denies the action, and the
   denial is returned to the model as a normal tool result so the loop can adapt
   rather than crash.
5. **An explicit `--auto-approve` escape hatch.** Trusted runs can bypass the
   prompt, with the appropriately understated help text: "Enable YOLO mode. Use
   at your own risk."
6. **A restrained Rich interface.** Model calls get a spinner; tool requests,
   results, errors, and final answers get readable panels; verbose mode includes
   arguments and token counts. The strings returned to the model stay plain
   text, so presentation does not leak into the agent protocol.

## Before And After

The course version relied on bare terminal output:

```text
 - Calling function: get_files_info({})
 -> - main.py: file_size=749 bytes, is_dir=False
Final Response
I found the project files.
```

The same flow is now separated into human-readable Rich panels (colour omitted
here, as README files remain stubbornly two-dimensional):

```text
╭───────────────────────────── Tool Call Verbose ──────────────────────────────╮
│  - Calling function: get_files_info({})                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────── Tool Result ─────────────────────────────────╮
│ - main.py: file_size=749 bytes, is_dir=False                                 │
│ - tests.py: file_size=1434 bytes, is_dir=False                               │
│ - README.md: file_size=12 bytes, is_dir=False                                │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────── Final Response ───────────────────────────────╮
│ I found the project files.                                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

More importantly, a write that previously ran immediately now stops for human
approval:

```text
Need approval to run write_file, {'file_path': 'test.txt', 'content': 'hello'}
Approve [y/N]?: n

╭───────────────────────────── Tool Call Denied ───────────────────────────────╮
│  - write_file cancelled by user                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

The model receives `Error: Action cancelled by user: write_file` and can respond
accordingly. A refusal is part of the conversation, not a trapdoor beneath it.

## How It Works

The agent currently uses `google/gemini-2.5-flash`, fixed in the source rather
than selected through the CLI. Prompts, conversation history, file contents,
directory listings, and tool results may all be sent to that model through
OpenRouter. This is another reason not to use sensitive data as test material.

Each turn through the loop:

1. Sends the system prompt, conversation history, and four tool schemas to the
   model through OpenRouter's OpenAI-compatible API.
2. Appends the model response to the message history.
3. Executes any requested tools after path validation and, where required,
   human approval.
4. Appends each plain-text tool result to the history so the model can inspect
   what happened and choose its next action.
5. Stops when the model returns a final response, or exits after 20 turns.

The model can request four tools:

| Tool | Purpose |
|---|---|
| `get_files_info` | List files and directories with sizes |
| `get_file_content` | Read a file, truncated at `MAX_CHARS` |
| `write_file` | Write or overwrite a whole file, creating parent directories |
| `run_python_file` | Execute a Python file with optional arguments and a 30-second timeout |

## Installation

Requires Python 3.10+, [`uv`](https://docs.astral.sh/uv/), and an OpenRouter API
key.

```bash
git clone https://github.com/Linux-Alchemy/ai_agent.git
cd ai_agent
uv sync --extra dev
```

Add the API key to a `.env` file in the repository root:

```dotenv
OPENROUTER_API_KEY=your_key_here
```

The file is ignored by Git. It should remain that way; secrets make poor
portfolio decorations.

## Running The Agent

Run from the repository root because the configured working directory is the
local `calculator/` project.

```bash
uv run python -m ai_agent.main "list the files"
uv run python -m ai_agent.main "fix the calculator bug" --verbose
```

Use `--auto-approve` only when you deliberately want writes and Python execution
to proceed without confirmation:

```bash
uv run python -m ai_agent.main "run the tests and fix the bug" --auto-approve
```

## Running The Tests

```bash
uv run python -m pytest -v
```

At the end of the core build this reports 14 passed and 2 skipped. The skipped
tests are placeholders for the optional prompt-injection work, not hidden test
failures.

## Project Layout

```text
ai_agent/
├── main.py                       # repository-root launcher
├── calculator/                   # fixed working directory and toy target app
├── src/ai_agent/
│   ├── main.py                   # CLI and agent loop
│   ├── call_functions.py         # schemas, dispatch, approval, Rich output
│   ├── approval.py               # default-deny human approval gate
│   ├── sandbox.py                # shared path resolution and containment
│   ├── config.py                 # WORKING_DIR and content limit
│   ├── prompts.py                # system prompt
│   └── functions/                # four model-callable tools
├── tests/                        # pytest suite and optional injection stubs
└── pyproject.toml
```

## Known Limitations

- **No process isolation.** `run_python_file` starts an ordinary subprocess with
  the current user's permissions. The path to the script is checked; what that
  script does after launch is not contained.
- **No network isolation.** Executed code can make network requests if the host
  allows them.
- **The approval gate is a control, not a security boundary.** A user can approve
  a harmful action, and `--auto-approve` bypasses the gate entirely.
- **Prompt injection is untreated.** Tool output and file content are supplied to
  the model without an untrusted-data framing strategy. The optional mitigation
  work was deliberately deferred rather than presented as solved.
- **The working directory is fixed.** It resolves `./calculator` from the launch
  location, so the agent must be run from the repository root.
- **Writes replace whole files.** There is no targeted edit or patch tool, which
  increases the chance of unrelated content drifting during a small change.
- **The approval prompt assumes interactive stdin.** A closed or piped stdin can
  raise `EOFError` instead of failing closed cleanly. The prompt interaction is
  also not covered by the test suite; only the approval predicate is.
- **Data leaves the local machine.** Prompts and any context gathered by tools
  are sent through OpenRouter to the configured model. Path confinement does not
  provide data confidentiality.
- **There is no audit log, rollback mechanism, resource sandbox, or guarantee
  that the model's claimed fix is correct.** The tests help; they are not an
  oracle, despite pytest's occasional air of authority.

Bubblewrap is a possible future route to Linux process isolation using
namespaces and explicit bind mounts. It is not implemented here because a
half-understood sandbox is worse than an honestly absent one. A production tool
would need that boundary designed and tested properly, along with network and
resource controls, secret separation, auditability, and a considered response
to prompt injection.

There are many other directions this project could take: targeted edits, richer
run reports, durable history, model selection, better evaluations, and so on.
The stopping point is deliberate. The goal was to understand agent loops and
tool calling, then tighten and polish the course project enough to demonstrate
that understanding without pretending it had become a production platform.

## Credits

Built on the boot.dev *Build an AI Agent* capstone, then extended as a focused
hardening and polish exercise. The original loop came from the course; the path
hardening, tests, approval flow, terminal interface, and any remaining sharp
edges belong to this version.
