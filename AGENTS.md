# Repository Guidelines

## Project Structure & Module Organization
- Source: `src/resender/` with two main areas:
  - `apps/`: Modal entrypoints (e.g., `weekly_email.py`, `karpathy_daily_quote.py`, `hello_world.py`).
  - `emails/`: email utilities (e.g., `sender.py`).
- Tests: `tests/` with `test_*.py` modules.
- Packaging: src-layout; imports resolve via `pyproject.toml` (`pythonpath = ["src"]`).

## Build, Test, and Development Commands
- Setup (uv, recommended): `uv pip install -e ".[dev]"`
- Setup (pip): `python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"`
- Run locally: `modal run src/resender/apps/weekly_email.py` (or `apps/karpathy_daily_quote.py`).
- Deploy schedule: `modal deploy src/resender/apps/weekly_email.py`.
- Test: `pytest -q`
- Lint/format: `ruff check .` and `black .`

## Coding Style & Naming Conventions
- Python ≥ 3.11; 4‑space indentation; use type hints for public APIs.
- Line length 100 (`black`, `ruff` configured in `pyproject.toml`).
- Names: modules/files `snake_case`; classes `PascalCase`; functions/vars `snake_case`; constants `UPPER_CASE`.
- Keep functions small and documented when non‑trivial.

## Testing Guidelines
- Framework: `pytest` (configured with `testpaths = ["tests"]` and `pythonpath = ["src"]`).
- Naming: files `tests/test_*.py`; tests `def test_*`.
- Add tests for new code paths and edge cases; keep fast and deterministic.
- Run all tests with `pytest -q` or a single file with `pytest tests/test_sender.py -q`.

## Commit & Pull Request Guidelines
- Commits: follow Conventional Commits (e.g., `feat:`, `fix:`, `docs:`, `chore:`). Example: `fix: use Modal secret for Resend`.
- PRs: include what/why, linked issues, test coverage for changes, and any relevant screenshots or `modal run/deploy` output when altering schedules or email content.
- Ensure `ruff`/`black`/`pytest` pass before requesting review; keep PRs focused and small.

## Security & Configuration Tips
- Secrets: use Modal secret `resend-secret` containing `RESEND_API_KEY` (required by `sender.py`). Create via: `modal secret create resend-secret RESEND_API_KEY=YOUR_KEY`.
- Local runs: export `RESEND_API_KEY` or place it in a local `.env` (never commit secrets).
- Avoid logging API keys or full payloads; prefer minimal logs.

