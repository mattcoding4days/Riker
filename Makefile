all: install

.ONESHELL:
install:
	python3 -m venv riker-env
	source riker-env/bin/activate
	pip3 install -r requirements.txt
	sudo python3 install.py

update:
	git pull

uninstall:
	sudo rm /usr/local/bin/riker_run

clean:
	rm -rf riker-env

.PHONY: all install update clean
