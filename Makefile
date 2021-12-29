.PHONY: auto test docs clean

auto: build39

build36: PYTHON_VER = python3.6
build37: PYTHON_VER = python3.7
build38: PYTHON_VER = python3.8
build39: PYTHON_VER = python3.9
build310: PYTHON_VER = python3.10

build36 build37 build38 build39 build310: clean
	$(PYTHON_VER) -m venv venv
	. venv/bin/activate; \
	pip install -U pip setuptools wheel; \
	pip install -r requirements.txt; \
	pre-commit install

test:
	rm -f .coverage coverage.xml
	. venv/bin/activate; pytest

lint:
	. venv/bin/activate; pre-commit run --all-files --show-diff-on-failure

clean-docs:
	rm -rf docs/_build

docs: clean-docs
	. venv/bin/activate; cd docs; make html

live-docs: clean-docs
	. venv/bin/activate; sphinx-autobuild docs docs/_build/html

deep-clean-dry-run:
	git clean -xdn

deep-clean:
	git clean -xdf

clean-env:
	rm -rf venv .tox

clean: clean-dist
	rm -rf .pytest_cache ./**/__pycache__ .mypy_cache
	rm -f .coverage coverage.xml ./**/*.pyc

clean-dist:
	rm -rf dist build *.egg *.eggs *.egg-info

build-dist:
	. venv/bin/activate; \
	pip install -U flit; \
	flit build --setup-py

upload-dist:
	. venv/bin/activate; \
	flit publish --setup-py

publish: test clean build-dist upload-dist clean
