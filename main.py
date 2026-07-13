"""Root entry point: lets the agent be launched as `uv run main.py` from the repo root.

The real implementation lives in `src/ai_agent/main.py`. Running from the repo root
matters — the agent's sandbox is the relative path `./calculator`.
"""

from ai_agent.main import main

if __name__ == "__main__":
    main()
