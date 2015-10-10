.PHONY: clean-pyc clean-build clean

define VERSION_SCR
import pkg_resources
print(pkg_resources.require("djdt_flamegraph")[0].version)
endef

VERSION ?= $(shell python -c '$(VERSION_SCR)')

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage

lint:
	flake8 djdt_flamegraph tests

test:
	tox

tag:
	git tag $(VERSION)

coverage:
	coverage run --source djdt_flamegraph setup.py test
	coverage report -m
