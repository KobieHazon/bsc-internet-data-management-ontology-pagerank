.PHONY: check test

check:
	python3 scripts/check_repository.py

test:
	python3 -m unittest discover -s tests
