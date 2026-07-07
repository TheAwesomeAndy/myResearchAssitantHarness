# SPDX-License-Identifier: Apache-2.0

HARNESS_ROOT ?= .
PHRASE_FILE ?= harness/forbidden_phrases.txt
MAIN_TEX ?= manuscript/main.tex
LOG_FILE ?= $(MAIN_TEX:.tex=.log)
CSV_DIR ?= outputs
TABLE_MANIFEST ?= harness/table_manifest.yaml

.PHONY: harness-verify harness-phrases harness-paths harness-latex harness-citations harness-tables harness-table-manifest harness-fixtures

harness-verify: harness-phrases harness-paths harness-latex harness-citations harness-tables harness-table-manifest
	@echo "harness verification complete"

harness-phrases:
	python scripts/check_forbidden_phrases.py $(HARNESS_ROOT) --phrase-file $(PHRASE_FILE)

harness-paths:
	python tools/check_path_markers.py $(HARNESS_ROOT)

harness-latex:
	@if [ -f "$(MAIN_TEX)" ]; then python scripts/verify_latex.py $(MAIN_TEX); else echo "no manuscript found; skipping LaTeX build"; fi

harness-citations:
	@if [ -f "$(LOG_FILE)" ]; then python scripts/check_citations.py $(LOG_FILE); else echo "no LaTeX log found; skipping reference scan"; fi

harness-tables:
	@if [ -f "$(MAIN_TEX)" ] && [ -e "$(CSV_DIR)" ]; then python scripts/check_table_values.py $(MAIN_TEX) $(CSV_DIR); else echo "no manuscript/CSV pair found; skipping broad table scan"; fi

harness-table-manifest:
	@if [ -f "$(TABLE_MANIFEST)" ]; then python scripts/check_table_manifest.py $(TABLE_MANIFEST); else echo "no table manifest found; skipping manifest table check"; fi

harness-fixtures:
	python scripts/run_fixture_tests.py
