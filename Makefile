# The checks CI runs, for every plugin in plugins/. Needs only uv.
.PHONY: setup lint fix typecheck test check

setup: ## install the workspace and its dev tools into .venv
	uv sync --frozen --no-build

lint: ## ruff, without changing files
	uv run --frozen --no-build ruff check --no-fix .
	uv run --frozen --no-build ruff format --check .

fix: ## let ruff fix what it can
	uv run --frozen --no-build ruff check .
	uv run --frozen --no-build ruff format .

typecheck: ## mypy, strict
	uv run --frozen --no-build mypy

test: ## unit and integration tests, offline
	uv run --frozen --no-build pytest

check: lint typecheck test ## everything CI checks
