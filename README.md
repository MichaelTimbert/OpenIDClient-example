# OpenIDClient-example
A simple FastAPI server that use Keycloak to authenticate users.
This example is based on https://pyoidc.readthedocs.io/en/latest/examples/rp.html

## Prerequisites

You need docker to be installed.

## Run

To launch Keycloack and the Relying Party:
```
$ sudo make up
```


- Keycloak is accessible at http://127.0.0.1:8008, login/password is admin/admin
- RelyingParty is accessible at http://127.0.0.1:8000


## Clean up

To remove docker container do not forget to run
```
$ sudo make clean-docker
```
