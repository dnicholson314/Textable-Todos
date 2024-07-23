import requests

from configs.models import DiscordAuthToken, Config

from django.http import JsonResponse
from django.urls import reverse

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from todo.settings import DISCORD_BOT_PUBLIC_KEY, DISCORD_APPLICATION_ID, DISCORD_BOT_TOKEN

INTERACTION_TYPES = {
    "PING": 1,
    "APPLICATION_COMMAND": 2,
}

CALLBACK_TYPES = {
    "PONG": 1,
    "CHANNEL_MESSAGE_WITH_SOURCE": 4,
}

DISCORD_OAUTH2_TOKEN_URL = "https://discord.com/api/oauth2/token"

def _exchange_code(request, code):
    data = {
        'client_id': DISCORD_APPLICATION_ID,
        'client_secret': DISCORD_BOT_TOKEN,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': request.build_absolute_uri(reverse("receive_discord_auth")),
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post(DISCORD_OAUTH2_TOKEN_URL, data=data, headers=headers)
    r.raise_for_status()
    return r.json()

def _validate_request(request):
    verify_key = VerifyKey(bytes.fromhex(DISCORD_BOT_PUBLIC_KEY))

    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = request.body.decode("utf-8")

    try:
        return verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return False

def _process_user_response(data) -> JsonResponse:
    payload = {}
    if data["type"] == INTERACTION_TYPES["PING"]:
        payload = {
            "type": CALLBACK_TYPES["PONG"]
        }
    elif data["type"] == INTERACTION_TYPES["APPLICATION_COMMAND"]:
        payload = {
            "type": CALLBACK_TYPES["CHANNEL_MESSAGE_WITH_SOURCE"],
            "data": {
                "content": "Task received!"
            },
        }

    return JsonResponse(payload)

def _process_discord_auth(request, code):
    data = _exchange_code(request, code)
    config, _ = Config.objects.get_or_create(user=request.user)

    token = DiscordAuthToken(
        config=config,
        access_token=data["access_token"],
        expires_in=data["expires_in"],
        refresh_token=data["refresh_token"],
    )
    token.save()

    return True