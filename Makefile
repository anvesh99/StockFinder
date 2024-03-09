# Define variables
VENV_NAME := venv
PYTHON := python3
PIP := $(VENV_NAME)/bin/pip
PYTHON_INTERPRETER := $(VENV_NAME)/bin/python

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  create-venv         Create a virtual environment"
	@echo "  activate-venv       Activate the virtual environment"

# Create a virtual environment
.PHONY: create-venv
create-venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "Virtual environment created. To activate, run: source $(VENV_NAME)/bin/activate"

# Activate the virtual environment
.PHONY: activate-venv
activate-venv:
	@echo "Activating virtual environment..."
	@source $(VENV_NAME)/bin/activate
