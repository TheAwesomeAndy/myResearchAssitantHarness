# SPDX-License-Identifier: Apache-2.0

MAIN_TEX ?= manuscript/main.tex

.PHONY: academic-check

academic-check:
	python scripts/qgate.py $(MAIN_TEX)
	python scripts/check_heading.py $(MAIN_TEX)
	python scripts/check_summary.py $(MAIN_TEX)
	python scripts/check_signals.py $(MAIN_TEX)
