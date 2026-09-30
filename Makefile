.PHONY: help format lint typecheck test clean

PYTHON_BIN ?= uv run python

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

format: ## Format all Python code (ruff: import sorting + formatting)
	$(PYTHON_BIN) -m ruff check --fix --select I .
	$(PYTHON_BIN) -m ruff format .

lint: typecheck ## Lint (ruff) and type-check all Python code
	$(PYTHON_BIN) -m ruff check .
	$(PYTHON_BIN) -m ruff format --check .

typecheck: ## Type-check with mypy
	$(PYTHON_BIN) -m mypy .

test: ## Run the test suite
	uv run pytest

clean: format lint ## Format then lint everything

check_release:
ifndef VERSION
	$(error VERSION is undefined)
endif

release: check_release
	git flow release start $(VERSION)
	sed -i 's/^version =.*/version = "$(VERSION)"/' pyproject.toml
	git add pyproject.toml
	git commit -m "Bump version to $(VERSION)"
	git flow release finish -m "Release $(VERSION)" $(VERSION) > /dev/null
