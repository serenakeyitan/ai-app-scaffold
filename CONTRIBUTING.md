# Contributing to ai-app-scaffold

Thank you for your interest in contributing! This project aims to make it trivially easy to scaffold production-ready AI applications.

## Development Setup

```bash
git clone https://github.com/serenakeyitan/ai-app-scaffold.git
cd ai-app-scaffold
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/ -v
```

## Adding a New Provider

1. Add the provider info to the appropriate dict in `src/ai_scaffold/providers.py`
2. Update the template logic in `src/ai_scaffold/templates.py` if needed
3. Add tests in `tests/test_providers.py`
4. Update `README.md` with the new provider in the supported providers table

## Code Style

- Python 3.10+, type hints everywhere
- `ruff` for linting: `ruff check .`
- Keep CLI output clean and helpful — use `rich` for formatting

## Submitting a PR

1. Fork the repo
2. Create a branch: `git checkout -b feat/my-feature`
3. Make your changes with tests
4. Open a PR against `main`
