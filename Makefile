.PHONY: install run project build publish package-install lint

install:
	uv sync

run:
	uv run database

project:
	uv run project

build:
	uv build

publish:
	uvx twine check dist/*

package-install:
	uv tool install --force dist/*.whl

lint:
	uv run ruff check .
