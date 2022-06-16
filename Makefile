SHELL := /bin/bash

PYTHON ?= python3.10
ENV_DIR ?= venv

default: behave

.PHONY: venv-init
venv-init:
	if [ ! -d "$(ENV_DIR)" ] ; then $(PYTHON) -m venv "$(ENV_DIR)" ; fi

.PHONY: pip-install
pip-install: venv-init
	@source "$(ENV_DIR)/bin/activate"
	python -m pip install --upgrade pip
	python -m pip install --editable .

test: unit-test

.PHONY: unit-test
unit-test:
	@source "$(ENV_DIR)/bin/activate"
	pytest

.PHONY: behave
behave:
	@source "$(ENV_DIR)/bin/activate"
	behave

.PHONY: clean
clean:
	rm -rf "$(ENV_DIR)" "./*.egg-info" || true
