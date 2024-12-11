.PHONY: clean install test lint format type-check security-check all

# Variables
PYTHON := python3.9
VENV := venv
REQUIREMENTS := requirements.txt
DEV_REQUIREMENTS := dev_requirements.txt

# Create virtual environment and install dependencies
install:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r $(REQUIREMENTS) && \
	pip install -r $(DEV_REQUIREMENTS)

# Clean up temporary files and build artifacts
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .coverage htmlcov/

# Run all tests
test:
	pytest --cov=. --cov-report=html

# Run linters
lint:
	pylint **/*.py
	flake8 .

# Format code
format:
	black .
	isort .

# Run type checking
type-check:
	mypy .

# Run security checks
security-check:
	bandit -r .
	safety check

# Run all checks and tests
all: clean format lint type-check security-check test