# SPDX-License-Identifier: Apache-2.0

HARNESS_ROOT ?= .
PHRASE_FILE ?= harness/forbidden_phrases.txt

.PHONY: harness-verify harness-phrases harness-paths

harness-verify: harness-phrases harness-paths
	@echo "harness verification complete"

harness-phrases:
	python scripts/check_forbidden_phrases.py $(HARNESS_ROOT) --phrase-file $(PHRASE_FILE)

harness-paths:
	python tools/check_path_markers.py
