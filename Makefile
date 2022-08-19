install-nodejs:
	sudo bash ./bash_scripts/install_nodejs.sh

create-environment:
	sudo apt-get update && sudo apt-get install virtualenv -y
	virtualenv ./venv --python /usr/bin/python3
	./venv/bin/pip install -r requirements.txt

create-files:
	./venv/bin/python3 run.py

start-services:
	bash ./output/start_services.sh

check-services:
	cat ./output/services_output.txt

