.PHONY: report analyze test html clean

PY := python

ERR := errors.log
LOG := log.txt
REPORTS_DIR := reports
HTML := $(REPORTS_DIR)/pytest_report.html
ANALYSIS := $(REPORTS_DIR)/error_analysis.txt

report:
	rm -f $(ERR) $(LOG)
	$(PY) tools/run_demo.py

analyze:
	mkdir -p $(REPORTS_DIR)
	bash ./analyze_log.sh $(ERR) | tee $(ANALYSIS)

test:
	$(PY) -m pytest -v

html:
	mkdir -p $(REPORTS_DIR)
	$(PY) -m pytest -v --html=$(HTML) --self-contained-html

clean:
	rm -f $(ERR) $(LOG)
	rm -f $(ANALYSIS) $(HTML)
	rm -rf .pytest_cache __pycache__ bambusim/__pycache__ test/__pycache__ web/__pycache__
