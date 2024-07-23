from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from todo.settings import env

from urllib import parse
import uuid

from todo.settings import DISCORD_APPLICATION_ID

DISCORD_OAUTH2_AUTH_URL = "https://discord.com/oauth2/authorize"

URL_PARAMS = {
    "client_id": DISCORD_APPLICATION_ID,
    "response_type": "code",
    "scope": "identify",
}

@login_required
def user_config_general(request):
    if request.method != "GET":
        return HttpResponseNotAllowed("GET")

    return render(request, 'configs/general.html')

def initiate_discord_auth(request):
    state = str(uuid.uuid4())
    request.session['oauth2_state'] = state

    params = URL_PARAMS
    params["state"] = state
    params["redirect_url"] = reverse("receive_discord_auth")
    url_encoded_params = parse.urlencode(params)

    auth_url = f"{DISCORD_OAUTH2_AUTH_URL}?{url_encoded_params}"

    return redirect(auth_url)
