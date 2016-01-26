lint:
	flake8 git-partial-lint.py lib/*.py tests/*.py

test:
	python -m unittest
