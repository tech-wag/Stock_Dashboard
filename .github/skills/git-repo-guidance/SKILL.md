---
name: repo-governance
description: Helps decide which files should be committed to Git and which should be ignored for this Stock Dashboard repository.
---

# Repository Governance Skill

Use this skill whenever you need to prepare changes for Git in this repository.

## What to commit
- Application source code under app/ and frontend/
- Test files under tests/
- Project documentation and metadata such as README.md, ARCHITECTURE.md, and requirements.txt
- Environment templates such as .env.example

## What to ignore
- Local secrets and runtime config such as .env
- Local virtual environments such as .venv/, venv/, env/, and ENV/
- Python caches and bytecode files such as __pycache__/, *.py[cod], .pytest_cache/, and .mypy_cache/
- Local databases and logs such as *.sqlite3 and *.log
- Editor and OS-specific files such as .DS_Store, .idea/, and .vscode/

## Guardrails
- Keep the repository reproducible by committing dependency and configuration files.
- Never commit API keys, tokens, or real secrets.
- If a new generated or local-only artifact appears, add it to .gitignore instead of tracking it.
- Prefer a minimal, clean commit set that supports collaboration and local setup.
