SHELL := /bin/bash

DATA_DIR   := data
INSTALL_PY    := install.py
REQUIREMENTS  := requirements.txt
FILTER_PY  := filter.py
RUNBASE_PY := NIR.main
RUNFAIR_PY := NIR_fairness_improvement.main
RUNFAIRALL_PY := NIR_fairness_improvement_all_together.prg_main

PYTHON ?= python3
ARGS ?=

.PHONY: help install libs filter runbase runfair runfairall clean

help:
	@echo "Targets:"
	@echo "  install    - скачать и распаковать данные (через install.py) в $(DATA_DIR)"
	@echo "  libs       - установить зависимости из $(REQUIREMENTS)"
	@echo "  filter     - запустить $(FILTER_PY)        (ARGS=\"...\")"
	@echo "  runbase    - запустить $(RUNBASE_PY)       (ARGS=\"...\")"
	@echo "  runfair    - запустить $(RUNFAIR_PY)       (ARGS=\"...\")"
	@echo "  runfairall - запустить $(RUNFAIRALL_PY)    (ARGS=\"...\")"
	@echo "  clean      - удалить метку распаковки и zip из $(DATA_DIR)"

install:
	@$(PYTHON) "$(INSTALL_PY)" --data-dir "$(DATA_DIR)" 

libs:
	@$(PYTHON) -m pip install -r "$(REQUIREMENTS)"

filter:
	@$(PYTHON) -m "$(FILTER_PY)" $(ARGS)

runbase:
	@$(PYTHON) -m "$(RUNBASE_PY)" $(ARGS)

runfair:
	@$(PYTHON) -m "$(RUNFAIR_PY)" $(ARGS)

runfairall:
	@$(PYTHON) -m "$(RUNFAIRALL_PY)" $(ARGS)

ZIP_NAME := hmda_2017_ca_all-records_labels.zip
STAMP    := $(DATA_DIR)/.hmda_2017_ca_unpacked.stamp

clean:
	@rm -f "$(STAMP)" "$(DATA_DIR)/$(ZIP_NAME)"
	@echo "Cleaned: $(STAMP) and $(DATA_DIR)/$(ZIP_NAME)"
