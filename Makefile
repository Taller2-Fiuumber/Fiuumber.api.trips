VENV := "venv"

# default target, when make executed without arguments
all: venv

# venv is a shortcut target
venv:
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt
	source $(VENV)/bin/activate

deactivate-venv:
	deactivate
	rm -rf $(VENV)

test:
	pip install pytest  --quiet
	pytest test

format:
	pip install black --quiet
	black **.py
	black src/*/*.py
	black test/*/*.py

	pip install flake8 --quiet
	flake8

.PHONY: all venv test format deactivate-venv
