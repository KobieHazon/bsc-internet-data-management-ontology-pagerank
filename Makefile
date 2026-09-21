.PHONY: check test

check: test

test:
	PYTHONPATH=src uv run --no-project --with-requirements requirements.txt python -B -m unittest discover -s tests

.PHONY: test-live
test-live:
	uv run --no-project --with-requirements requirements.txt python -B scripts/check_live.py
