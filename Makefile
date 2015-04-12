flake:
	flake8 weblib test

flake_verbose:
	flake8 weblib test --show-pep8

test:
	run test

coverage:
	coverage erase
	coverage run --source=weblib -m runscript.cli test
	coverage report -m

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete

doc:
	sh -c 'cd docs; make html'

upload:
	python setup.py sdist upload

.PHONY: all build venv flake test vtest testloop cov clean doc
