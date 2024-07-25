import requests

from pprint import pprint

from configs.models import Config
from tasks.models import Task

from datetime import datetime

from django.http import JsonResponse, HttpResponseServerError
from django.urls import reverse
from django.db import IntegrityError

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from todo.settings import DISCORD_BOT_PUBLIC_KEY, DISCORD_APPLICATION_ID, DISCORD_BOT_CLIENT_SECRET

INTERACTION_TYPES = {
    "PING": 1,
    "APPLICATION_COMMAND": 2,
}

CALLBACK_TYPES = {
    "PONG": 1,
    "CHANNEL_MESSAGE_WITH_SOURCE": 4,
}

BOT_RESPONSES = {
    "SUCCESS": "Task received!",
    "UNAUTHORIZED": "Unable to verify your account. Are you registered with the app?",
    "UNPROCESSED": "Unable to add task due to a server error. Make sure you formatted the date correctly!",
}

DISCORD_OAUTH2_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_OAUTH2_INFO_URL = "https://discord.com/api/oauth2/@me"

def _exchange_code(request, code):
    data = {
        'client_id': DISCORD_APPLICATION_ID,
        'client_secret': DISCORD_BOT_CLIENT_SECRET,
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

def _get_user_id_from_token(response):
    if not "access_token" in response:
        raise HttpResponseServerError("Unable to process request: token could not be retreived from dictionary")

    token = response["access_token"]
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    r = requests.get(DISCORD_OAUTH2_INFO_URL, headers=headers)
    r.raise_for_status()
    data = r.json()

    if "user" not in data:
        raise HttpResponseServerError("Unable to process request: user data not found") 
    user_id = data["user"]["id"]

    return user_id

def _verify_user_id_from_webhook_data(data):
    if "member" not in data:
        return False
    user_id = data["member"]["user"]["id"]
    try:
        config = Config.objects.get(discord_id=user_id)
    except Config.DoesNotExist:
        return False

    return config.user

def _add_task_for_user_from_webhook_data(user, data):
    if "data" not in data:
        return False
    task_data = data["data"]["options"]

    task = Task(user=user)

    for item in task_data:
        name = item["name"]
        value = item["value"]

        if name == "title":
            task.title = value
        elif name == "date":
            try:
                due_date = datetime.strptime(value, "%m-%d-%y")
            except ValueError:
                return False
            task.due_date = due_date

    task.save()
    return task

# there's definitely a better way to code this lmao
def _process_slash_command(data):
    payload = {
        "type": CALLBACK_TYPES["CHANNEL_MESSAGE_WITH_SOURCE"],
        "data": {
            "content": BOT_RESPONSES["SUCCESS"]
        },
    }

    user = _verify_user_id_from_webhook_data(data)
    if not user:
        payload["data"]["content"] = BOT_RESPONSES["UNAUTHORIZED"]
        return payload

    task = _add_task_for_user_from_webhook_data(user, data)
    if not task:
        payload["data"]["content"] = BOT_RESPONSES["UNPROCESSED"]
        return payload

    return payload

def process_discord_bot_webhook(data) -> JsonResponse:
    payload = {}
    if data["type"] == INTERACTION_TYPES["PING"]:
        payload = {
            "type": CALLBACK_TYPES["PONG"]
        }
    elif data["type"] == INTERACTION_TYPES["APPLICATION_COMMAND"]:
        payload = _process_slash_command(data)

    return JsonResponse(payload)

def process_discord_auth(request, code):
    response = _exchange_code(request, code)
    config, _ = Config.objects.get_or_create(user=request.user)

    user_id = _get_user_id_from_token(response)
    config.discord_id = user_id
    try:
        config.save()
    except IntegrityError:
        raise HttpResponseServerError("Unable to process request: Discord user already authenticated")

    return True

def validate_request(request):
    verify_key = VerifyKey(bytes.fromhex(DISCORD_BOT_PUBLIC_KEY))

    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = request.body.decode("utf-8")

    try:
        return verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return False
