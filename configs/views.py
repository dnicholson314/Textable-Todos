from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from todo.settings import env

from urllib import parse
import uuid

from todo.settings import DISCORD_APPLICATION_ID

from .models import Config

DISCORD_OAUTH2_AUTH_URL = "https://discord.com/oauth2/authorize"

URL_PARAMS = {
    "client_id": DISCORD_APPLICATION_ID,
    "response_type": "code",
    "scope": "identify",
}

@login_required
def user_config_general(request):
    try:
        config = Config.objects.get(user=request.user)
        discord_username = config.discord_username
    except Config.DoesNotExist:
        discord_username = ""

    context = {
        "discord_username": discord_username,
    }

    return render(request, 'configs/settings.html', context)

def initiate_discord_auth(request):
    state = str(uuid.uuid4())
    request.session['oauth2_state'] = state

    params = URL_PARAMS
    params["state"] = state
    params["redirect_url"] = reverse("receive_discord_auth")
    url_encoded_params = parse.urlencode(params)

    auth_url = f"{DISCORD_OAUTH2_AUTH_URL}?{url_encoded_params}"

    return redirect(auth_url)
