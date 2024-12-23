test:
	. .venv/bin/activate && pytest

install: prepare_setup
	python -m pip install "."
	@echo APPLICATION INSTALLED SUCCESSFULLY

reset_dev: prepare_setup install_dev

install_dev:
	python -m pip install -e ".[dev]"
	pre-commit install
	@echo DEV SETUP COMPLETED SUCCESSFULLY

prepare_setup: clean
	-deactivate
	rm -rvf .venv .tox
	python -m venv .venv
	. .venv/bin/activate
	python -m pip install --upgrade pip setuptools wheel build twine

clean:
	rm -rvf site htmlcov coverage-reports .coverage* dist build *.egg-info *.whl
	find . -type f -name "*.py[co]"
	find . -type d -name __pycache__
	find . -type f -name "*.py[co]" -delete
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.py[co]"
	find . -type d -name __pycache__

tidy:
	find . -type f -name "*.py[co]"
	find . -type d -name __pycache__
	find . -type f -name "*.py[co]" -delete
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.py[co]"
	find . -type d -name __pycache__

pipc:
	. .venv/bin/activate
	pip-compile --strip-extras --output-file=docs/requirements.txt pyproject.toml
	pip-compile --strip-extras --all-extras --output-file=docs/requirements-dev.txt pyproject.toml
	licensecheck

tox:
	. .venv/bin/activate
	tox --verbose

# Check application code complexity

cc:
	radon cc generator --total-average -nb

mi:
	radon mi generator -nb

radon: cc mi
	radon raw generator
	radon hal generator

-include *.mk
