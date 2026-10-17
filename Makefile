# SPDX-License-Identifier: Apache-2.0

PYTHON ?= python3
VALIDATION_DIR ?= work/local-validation

.PHONY: all validate test golden dashboard clean

all: clean validate test golden dashboard

validate:
	@mkdir -p $(VALIDATION_DIR)
	@$(PYTHON) scripts/validate-metadata --repo-root . \
		--output $(VALIDATION_DIR)/metadata-validation.json
	@$(PYTHON) scripts/validate-package-index --repo-root . \
		--output $(VALIDATION_DIR)/package-index-validation.json
	@$(PYTHON) ci/validate-repository.py --repo-root . \
		--output $(VALIDATION_DIR)/repository-validation.json

test:
	@$(PYTHON) -m unittest discover -s scripts/tests -v

golden:
	@rm -rf -- $(VALIDATION_DIR)/golden-sources
	@rm -f -- $(VALIDATION_DIR)/golden-materialization.json
	@mkdir -p $(VALIDATION_DIR)/golden-sources
	@$(PYTHON) scripts/golden-eval materialize --repo-root . \
		--manifests-dir tests/golden \
		--output-dir $(VALIDATION_DIR)/golden-sources \
		--output $(VALIDATION_DIR)/golden-materialization.json \
		--now 2026-08-08T00:00:00Z

dashboard:
	@rm -rf -- $(VALIDATION_DIR)/dashboard
	@rm -f -- $(VALIDATION_DIR)/dashboard-generation.json
	@mkdir -p $(VALIDATION_DIR)
	@$(PYTHON) scripts/generate-dashboard --repo-root . \
		--output-dir $(VALIDATION_DIR)/dashboard \
		--output $(VALIDATION_DIR)/dashboard-generation.json

clean:
	@rm -rf -- $(VALIDATION_DIR)
