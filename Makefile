.PHONY: install test run experiment demo
install:
	pip install -e '.[dev]'
test:
	pytest -q
run:
	uvicorn devassure.api:app --reload --port 8002
experiment:
	python scripts/run_ab.py
demo:
	python scripts/demo_analysis.py
