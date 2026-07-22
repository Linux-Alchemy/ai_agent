# ai_agent

A small AI coding agent, built as the capstone for boot.dev's *Build an AI Agent*
course. Give it a prompt; it explores a sandboxed directory, reads and writes
files, runs Python, and iterates until it has an answer — or has fixed your bug.

It's an agent in the honest sense: a loop around an LLM that can call tools, see
the results, and decide what to do next. About 200 lines all in.

## ⚠️ Security Warning

This project is for **learning purposes only**. The agent can read, write, and
**execute arbitrary Python code** within its configured working directory. It
lacks the guardrails a production AI agent would have — the only current
safeguards are working-directory confinement and a 30-second execution timeout.

**Do not distribute this program for others to use, and do not point it at
anything you care about.** Proper hardening is deferred to a later polish pass.

## Usage

Always run **from the repo root** — the agent's sandbox is the *relative* path
`./calculator`, so launching from anywhere else silently relocates it.

```bash
uv run main.py "how does the calculator render results to the console?"
uv run main.py "fix the bug: 3 + 7 * 2 shouldn't be 20" --verbose
```

`--verbose` prints the arguments passed to each tool, the result of each call,
and per-turn token counts. Worth having on while you're watching it think.

Requires `OPENROUTER_API_KEY` in a `.env` file at the repo root. See `.env.example`.

## How it works

`main.py` holds the agent loop. Each pass:

1. Send the conversation (plus the four tool schemas) to the model.
2. Append the model's reply to the message history.
3. If it asked for no tools, print its answer and stop — it's done.
4. Otherwise run each requested tool and append the result as a `tool` message,
   so the model can see what happened.
5. Repeat, up to 20 turns, then give up with exit code 1.

The message history is the agent's entire memory. Everything it learns — every
directory listing, every file it reads, every test run — accumulates there, which
is why prompt token counts climb steeply as it works.

## Tools

The model can call four functions. Each one is confined to the sandbox directory,
which is injected server-side and never exposed to the model.

| Tool | Does |
|---|---|
| `get_files_info` | List files and directories, with sizes |
| `get_file_content` | Read a file (truncated at `MAX_CHARS`) |
| `write_file` | Write or overwrite a file, creating parents as needed |
| `run_python_file` | Execute a Python file with optional args, 30s timeout |

Every one validates that the resolved path stays inside the working directory
before touching the filesystem.

## Layout

```
main.py                      # launcher — imports and calls main()
src/ai_agent/
  main.py                    # the agent loop
  prompts.py                 # system prompt
  config.py                  # MAX_CHARS
  call_functions.py          # tool schemas + dispatch
  functions/                 # the four tools, one per file
tests/                       # print-based test modules
calculator/                  # the sandbox — a toy app for the agent to work on
```

Run the tests from the repo root: `uv run python tests/test_<name>.py`

## Known limitations

Kept here deliberately — this project is the base for something larger, and these
are the things that need fixing before it grows up.

- **The sandbox root is relative and hardcoded** (`"./calculator"`). It should be
  resolved to an absolute path once at startup and fail loudly if it doesn't exist.
  As it stands, launching from the wrong directory silently moves the sandbox — and
  `write_file` will happily conjure a fresh one into being. A sandbox is only as
  good as the thing that defines its boundary.
- **Whole-file writes only.** `write_file` overwrites whole files, so changing one
  line means the model regenerates the entire file from memory and may drift. A
  targeted-edit tool is deliberately outside the reduced project scope.
- **`run_python_file` shells out to the literal `"python"`** to satisfy the course
  grader. Should be `sys.executable` — the interpreter actually running the process.
- **No sanity check on what the model writes.** It can and will report success on a
  fix that breaks something else. The system prompt currently compels it to run the
  test suite first, which helps, but that's an instruction, not a guarantee.
