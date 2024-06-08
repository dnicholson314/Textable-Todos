from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from . import PUBLIC_KEY, INTERACTION_TYPES, CALLBACK_TYPES

import json

# Remember to update ngrok link in the settings for development!
# Eventually kick all the processing code (after verifying) to processors.py or services.py
# Maybe log all interactions in db?
# Create tests

def _validate_request(request):
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]
    body = request.body.decode("utf-8")

    try:
        return verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return False

@csrf_exempt
def test_webhook(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    if not _validate_request(request):
        return HttpResponse('Unauthorized', status=401)

    data_str = request.body.decode()
    data = json.loads(data_str)

    if "type" not in data:
        return HttpResponseBadRequest()

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