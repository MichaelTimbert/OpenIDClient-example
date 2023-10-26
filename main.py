from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic import rndstr
from oic.oic.message import AuthorizationResponse
#from oic.utils.http_util import Redirect
from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection

import requests
import time

KEYCLOAK_URL = "http://localhost:8080"

RP_URL = "http://localhost:8000"


client = Client(client_authn_method=CLIENT_AUTHN_METHOD)


@asynccontextmanager
async def setup(app: FastAPI):
    """ Register this RP as a Client in Keycloak """

    wait_for_keycloak()

    provider_info = client.provider_config(KEYCLOAK_URL+"/realms/master")

    #for info in provider_info:
    #    print(info, provider_info[info])

    args = {
        "redirect_uris": [RP_URL+"/fromProvider"],
        "contacts": ["foo@example.com"]
        }


    # Create initial_access_token on Keycloak
    # to allow this RP to register as Client
    keycloak_connection = KeycloakOpenIDConnection(server_url= KEYCLOAK_URL,username="admin",password="admin",realm_name="master")
    keycloak_admin = KeycloakAdmin(connection=keycloak_connection)
    initial_access_token = keycloak_admin.create_initial_access_token()

    print(initial_access_token)


    registration_response = client.register(
        provider_info["registration_endpoint"],
        registration_token=initial_access_token['token'],
        **args)

    print("registration response:")
    for i in registration_response:
        print(f"\t{i}\t{registration_response[i]}")

    yield

    print("Nothing to do on shutdown")


def wait_for_keycloak():
    """ Wait for keycloak to be ready, this can take up to 20 seconds"""
    while True:
        try:
            r = requests.get(KEYCLOAK_URL)
        except:
            time.sleep(2)
            print("waiting for Keycloak: connection to %s failed"%KEYCLOAK_URL)
            continue
        
        if r.status_code == 200:
            print("Keycloak ready ! ")
            break

templates = Jinja2Templates(directory="templates")

app = FastAPI(lifespan=setup)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/login")
async def login(request: Request):
    session = {}
    session["state"] = rndstr()
    session["nonce"] = rndstr()
    args = {
        "client_id": client.client_id,
        "response_type": "code",
        "scope": ["openid"],
        "nonce": session["nonce"],
        "redirect_uri": client.registration_response["redirect_uris"][0],
        "state": session["state"]
    }

    auth_req = client.construct_AuthorizationRequest(request_args=args)
    login_url = auth_req.request(client.authorization_endpoint)
    print("redirection to:", login_url)
    return RedirectResponse(url=login_url)

@app.get("/fromProvider")
async def fromprovider(request: Request):
    print(request.query_params)
    info = "%s"%request.query_params
    aresp = client.parse_response(AuthorizationResponse, info=info, sformat="urlencoded")
    print("aresp: ",aresp)

    code = aresp["code"]
    #assert aresp["state"] == session["state"]
    args = {
        "code": aresp["code"]
    }

    resp = client.do_access_token_request(state=aresp["state"],
                                        request_args=args,
                                        authn_method="client_secret_basic")
    print(resp)

    userinfo = client.do_user_info_request(state=aresp["state"])

    return userinfo