serv:
	uvicorn main:app --reload --port 8081

venv:
	python3 -m venv $@
	$@/bin/pip3 install -r requirement.txt

up:
	docker-compose up --build

clean-docker:
	docker-compose down
	docker image rm relyingparty
	docker image rm quay.io/keycloak/keycloak:20.0.0
