# SPDX-License-Identifier: Apache-2.0

HARNESS_ROOT ?= .
PHRASE_FILE ?= harness/forbidden_phrases.txt
# Main LaTeX source; override from command line as needed
MAIN_TEX ?= manuscript/main.tex
# Log file used for citation scanning
LOG_FILE ?= $(MAIN_TEX:.tex=.log)
# Directory (or file) containing CSVs with source data
CSV_DIR ?= outputs

.PHONY: harness-verify harness-phrases harness-paths harness-latex harness-citations harness-tables

# Run all harness checks. Each subtarget returns non-zero on failure.
harness-verify: harness-phrases harness-paths harness-latex harness-citations harness-tables
	@echo "harness verification complete"

# Scan for disallowed phrases in supported file types
harness-phrases:
	python scripts/check_forbidden_phrases.py $(HARNESS_ROOT) --phrase-file $(PHRASE_FILE)

# Scan files for restricted path markers
harness-paths:
	python tools/check_path_markers.py

# Compile LaTeX manuscript and report build errors
harness-latex:
	python scripts/verify_latex.py $(MAIN_TEX)

# Compile and then scan the LaTeX log for undefined citations/references
harness-citations:
	# Recompile to produce fresh log before scanning citations
	python scripts/verify_latex.py $(MAIN_TEX)
	python scripts/check_citations.py $(LOG_FILE)

# Compare numeric table values in the manuscript against CSV source data
harness-tables:
	python scripts/check_table_values.py $(MAIN_TEX) $(CSV_DIR)
