serv:
	uvicorn main:app --reload

venv:
	python3 -m venv $@
	$@/bin/pip3 install -r requirement.txt

