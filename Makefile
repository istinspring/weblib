flake:
	flake8 weblib test

flake_verbose:
	flake8 weblib test --show-pep8

test:
	py.test

coverage:
	py.test --cov weblib --cov-report term-missing

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete

doc:
	sh -c 'cd docs; make html'

upload:
	python setup.py sdist upload

.PHONY: all build venv flake test vtest testloop cov clean doc
