# ai_agent v2 — Hardening & Polish Pass

> **What this is:** the continuation of the boot.dev *Build an AI Agent*
> capstone. The course built the engine; this pass is about extending that
> learning — deeper exploration of the same concepts — with the end goal of
> a polished project ready for display as a genuine portfolio piece.

## What

Take the existing agent (`Linux-Alchemy/ai_agent`, ~200 lines, four tools,
working-directory sandbox) and evolve it through three focused upgrades across
three core phases:

1. **Safety net** — migrate print-based tests to basic pytest; fix the
   sandbox root and close symlink escapes.
2. **Control** — add an approval gate for writes and execution, with
   `--auto-approve` for trusted runs.
3. **Polish** — add a restrained Rich terminal interface and finish the README.

After the core build, one **Optional** security showcase remains: reproduce an
indirect prompt-injection attack, add prompt/result-framing mitigations, and
document their limitations. It can be skipped without leaving the core project
incomplete.

OS-level process isolation is outside the current build. Bubblewrap (`bwrap`) is
recorded in `PLAN.md` as a possible future hardening upgrade once its namespace
and bind-mount model can be implemented and verified properly.

## Why

- **Portfolio:** transform "followed a course" into "took a deliberately
  unsafe agent and hardened it, with receipts" — aligned with an AI
  security career target.
- **Learning:** each phase is a continued lesson building on the last,
  worked through tutor-style. The git history documents the journey.

## Stack & Conventions

- Python 3.13, `uv`, src layout (existing). OpenRouter via OpenAI SDK.
- pytest for testing; Rich for output.
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

- All three core upgrades are complete, with each phase passing its checkpoint.
- README explains how to run the agent, what was hardened, and which limitations
  remain. If the optional showcase is completed, it also documents the injection
  demo from attack through mitigation and test.
- `uv run python -m pytest -v` green; agent still fixes the calculator bug.
