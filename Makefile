.PHONY: help install test lint up-postgres up-smart-contract

help:
	@echo "Targets:"
	@echo "  install          Install runtime + dev dependencies"
	@echo "  test             Run pytest (CI-compatible)"
	@echo "  lint             Run Ruff"
	@echo "  up-postgres      Start API with PostgreSQL backend"
	@echo "  up-smart-contract Start API with Hardhat smart-contract backend"

install:
	pip install -r requirements-dev.txt

test:
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -v

lint:
	ruff check app tests

up-postgres:
	docker compose --profile postgres up --build

up-smart-contract:
	docker compose --profile smart_contract up --build
