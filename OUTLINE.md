# ai_agent v2 — Hardening & Polish Pass

> **What this is:** the continuation of the boot.dev *Build an AI Agent*
> capstone. The course built the engine; this pass is about extending that
> learning — deeper exploration of the same concepts — with the end goal of
> a polished project ready for display as a genuine portfolio piece.

## What

Take the existing agent (`Linux-Alchemy/ai_agent`, ~200 lines, four tools,
working-directory sandbox) and evolve it through eight deliberate upgrades
across four phases:

1. **Safety net** — migrate print-based tests to basic pytest; fix the
   sandbox root and close symlink escapes.
2. **Control** — approval gate for writes/execution (`--auto-approve` to
   skip); a targeted `edit_file` tool with diff output.
3. **Security showcase** — a documented prompt-injection attack and its
   mitigation; a Bubblewrap process boundary around code execution.
4. **Polish** — Rich terminal interface; end-of-run report with JSONL
   audit logging.

## Why

- **Portfolio:** transform "followed a course" into "took a deliberately
  unsafe agent and hardened it, with receipts" — aligned with an AI
  security career target.
- **Learning:** each phase is a continued lesson building on the last,
  worked through tutor-style. The git history documents the journey.

## Stack & Conventions

- Python 3.13, `uv`, src layout (existing). OpenRouter via OpenAI SDK.
- pytest for testing; Bubblewrap (`bwrap`) for isolation; Rich for output.
- Arch Linux (Omarchy), Neovim.

## Constraints

- **Lean above all.** No unnecessary code, no speculative abstraction.
  Clean, minimal, readable — every line earns its place.
- **Honest skill representation.** Pytest usage stays at genuine beginner
  level: plain test functions, simple asserts, `tmp_path`, maybe one
  fixture. No parametrize gymnastics, no mocking frameworks.
- **Holes are expected and acceptable.** This is a learning artifact, not
  a production system. Known gaps get documented in the README, not
  papered over.

## Done Means

- All eight upgrades merged, each phase a commit checkpoint.
- README updated per phase: limitations list evolves into a changelog of
  fixes, plus the documented injection demo (attack → mitigation → test).
- `uv run python -m pytest -v` green; agent still fixes the calculator bug.
