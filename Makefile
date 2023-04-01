INFRA_DIR = infra

.PHONY: build package deploy setup

build:
	pip-compile requirements.in
	pip3 install --target ${INFRA_DIR}/package -r requirements.txt

package:
	cp -r demo/* ${INFRA_DIR}/package/
	cd ${INFRA_DIR}/package/ && zip -r ../passenger_service.zip .

deploy:
	cd ${INFRA_DIR} && terraform init && terraform apply -auto-approve

setup:
	python3 -m venv __venv__
	
clean:
	cd ${INFRA_DIR} && terraform destroy -auto-approve
	rm -rf ${INFRA_DIR}/package
	rm -f ${INFRA_DIR}/passenger_service.zip
	rm -f requirements.txt
	

all: build package deploy