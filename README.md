# AI Software Factory

Phase 0 baseline scaffold for a CLI-first AI software factory.

## Quickstart

```bash
pyenv install 3.13.12 --skip-existing
pyenv local 3.13.12
python -m venv .venv
source .venv/bin/activate
pip install -e .
factory
factory status
factory chat --message "hello"
factory --session-id <session_id>
factory chat --session-id <session_id>
```

## Python Version
- Required: `3.13.12`
- Supported range: `>=3.13,<3.14` (LangGraph dependency compatibility)

## Session Resume
- When chat exits, the CLI prints `Session saved: <session_id>`.
- Resume a session with:
  - `factory --session-id <session_id>` (interactive default)
  - `factory chat --session-id <session_id>`

## Layout
- `src/factory/`: CLI, config, logging, session primitives
- `configs/factory.toml`: provider/model configuration
- `docs/`: architecture notes and ADRs
- `tests/`: baseline tests
