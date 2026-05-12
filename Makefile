.PHONY: install run test test-api test-ui lint clean

install:
	pip install -r backend/requirements.txt
	playwright install --with-deps chromium

run:
	cd backend && uvicorn app:app --reload --host 0.0.0.0 --port 8888

test:
	pytest tests/ -v -n auto --reruns 2 --alluredir=allure-results

test-api:
	pytest tests/test_api_*.py -v

test-ui:
	pytest tests/test_ui_*.py -v --browser=chromium

lint:
	ruff check backend/ tests/

clean:
	rm -rf __pycache__ test-results/ allure-results/ allure-report/
