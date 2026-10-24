# The checks CI runs, for every plugin in plugins/. Needs only uv.
.PHONY: setup lint fix typecheck test check

setup: ## install the workspace and its dev tools into .venv
	uv sync --frozen

lint: ## ruff, without changing files
	uv run --frozen ruff check --no-fix .
	uv run --frozen ruff format --check .

fix: ## let ruff fix what it can
	uv run --frozen ruff check .
	uv run --frozen ruff format .

typecheck: ## mypy, strict
	uv run --frozen mypy

test: ## unit and integration tests, offline
	uv run --frozen pytest

check: lint typecheck test ## everything CI checks
