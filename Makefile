all: format test start-services exec

test:
	pip install pytest --quiet
	pytest --cov=src/domain --cov=src/services tests/

format:
	pip install black --quiet
	black **.py
	black src/*/*.py
	black tests/*.py

	pip install flake8 --quiet
	flake8

coverage:
	pip install coverage --quiet
	coverage report --fail-under=75 -m

start-services:
	docker-compose up --build --force-recreate -d

stop-services:
	docker-compose down

exec:
	docker exec -it fiuumberapitrip_web_1 sh

run:
	python -m uvicorn main:app --reload --host 0.0.0.0 --port 8080

.PHONY: all test format start-services stop-services
