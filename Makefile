flake:
	flake8 tools test

flake_verbose:
	flake8 tools test --show-pep8

test:
	run test

coverage:
	coverage erase
	coverage run --source=tools -m runscript.cli test
	coverage report -m

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete

upload:
	python setup.py sdist upload

.PHONY: all build venv flake test vtest testloop cov clean doc
