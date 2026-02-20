# Starray

Phase 0 baseline scaffold for a CLI-first StarRay.

## Install (pipx package)

```bash
pipx install --python 3.13 starray-cli
starray --version
starray init
```

To enable remote provider calls (OpenAI/Anthropic/Gemini via LiteLLM):

```bash
pipx inject starray-cli "starray-cli[providers]"
export ANTHROPIC_API_KEY="your_key_here"   # or OPENAI_API_KEY / GEMINI_API_KEY
starray --config ~/.config/starray/starray.toml
```

## Local Development Install

```bash
git clone <repo-url>
cd starray
pyenv install 3.13.12 --skip-existing
pyenv local 3.13.12
python -m venv .venv
source .venv/bin/activate
pip install -e ".[providers]"
export ANTHROPIC_API_KEY="your_key_here"   # or OPENAI_API_KEY / GEMINI_API_KEY
starray
starray status
starray provider
starray chat --message "hello"
starray --session-id <session_id>
starray chat --session-id <session_id>
```

When running from source, prefer:

```bash
python -m starray.cli --config configs/starray.toml
```

This avoids accidentally invoking a global `starray` binary.

## Python Version
- Required: `3.13.12`
- Supported range: `>=3.13,<3.14` (LangGraph dependency compatibility)

## Session Resume
- When chat exits, the CLI prints `Session saved: <session_id>`.
- Resume a session with:
  - `starray --session-id <session_id>` (interactive default)
  - `starray chat --session-id <session_id>`

## Config Resolution
Order of precedence:
1. `--config <path>`
2. `STARRAY_CONFIG` environment variable
3. `~/.config/starray/starray.toml` (or `$XDG_CONFIG_HOME/starray/starray.toml`)
4. `./configs/starray.toml` (repo-local fallback)

If no config exists, run `starray init`.

## Troubleshooting Provider Fallbacks
- If output shows `[provider] local/...`, a remote provider call failed and Starray used fallback.
- Starray now shows one `[fallback] ...` reason line in the Analyst panel instead of raw LiteLLM banners.
- Verify the active config and route:
  - `starray status`
  - `starray provider`
- For pipx installs, ensure provider extras are injected:
  - `pipx inject starray-cli "starray-cli[providers]"`
- For local dev installs, ensure extras are installed in the active venv:
  - `pip install -e ".[providers]"`
- Confirm the API key exists in the same shell where you run Starray:
  - `echo "$ANTHROPIC_API_KEY" | wc -c`

## Interactive Commands
- `/status`: show active provider/model.
- `/provider`: show provider/model fallback routing.
- `/session`: show current session id.
- `/help`: show available chat commands.
- `exit` or `quit`: save and exit.

## Release
- CI runs on pushes/PRs via `.github/workflows/ci.yml`.
- Publishing runs on tags like `v0.1.2` via `.github/workflows/publish.yml`.
- PyPI publishing uses repository secret `PYPI_API_TOKEN`.
- A helper installer script is available at `scripts/install.sh`.

## Layout
- `src/starray/`: CLI, config, logging, session primitives
- `configs/starray.toml`: provider/model configuration
- `docs/`: architecture notes and ADRs
- `tests/`: baseline tests
