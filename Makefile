# The checks CI runs, for every plugin in plugins/. Needs only uv.
.PHONY: setup lint fix typecheck test coverage check

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

coverage: ## the tests, measured; fails below 80, where the public repos' badge turns red
	uv run --frozen coverage run --source=plugins/heinzel-sf/src --branch -m pytest
	uv run --frozen coverage report --fail-under=80

check: lint typecheck test ## everything CI checks
