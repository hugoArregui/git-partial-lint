lint:
	flake8 git-partial-lint.py lib/*.py tests/*.py

test:
	python -m unittest

coverage:
	rm -rf .coverage htmlcov
	coverage run -m unittest
	coverage html

