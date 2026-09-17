# Insightful 4.0 — verification entrypoints. `make check` is the gate.
PY := .venv-renderer/bin/python

.PHONY: check test golden cohort baseline venv

check: test golden cohort ## full gate: tests + golden checksums + cohort text diff

test:
	$(PY) -m pytest tests/ -q

golden:
	./regression.sh --verify

cohort:
	./tools/cohort_diff.sh

baseline: ## re-capture the cohort baseline (deliberate act — review the diff first)
	./tools/cohort_run.sh _baseline

venv: ## rebuild the runtime from scratch
	python3 -m venv .venv-renderer
	.venv-renderer/bin/pip install -q -r requirements-pipeline.txt
