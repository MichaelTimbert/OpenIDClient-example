# OpenIDClient-example
A simple FastAPI server that use Keycloak to authenticate users.

## Run

To launch Keycloack and the Relying Party:
```
$ sudo docker-compose up
```

- Keycloak is accessible at http://127.0.0.1:8008, login/password is admin/admin
- RelyingParty is accessible at http://127.0.0.1:8000


To remove docker container do not forget to run
```
$ sudo docker-compose down
```
