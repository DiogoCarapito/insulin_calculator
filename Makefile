install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -v --cov=main tests/*.py

format:
	black . *.py

lint:
	pylint --disable=R,C main.py

all: install lint test format
