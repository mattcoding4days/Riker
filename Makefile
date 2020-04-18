all: env install

.ONESHELL:
env:
	python3 -m venv riker-env
	source riker-env/bin/activate
	pip3 install -r requirements.txt

install:
	source riker-env/bin/activate
	sudo python install.py

update:
	git pull

.PHONY: all env install update
