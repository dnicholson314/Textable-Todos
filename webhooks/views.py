from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .services import validate_request, process_discord_bot_webhook, process_discord_auth

import json

# Log all interactions in db
# Create tests

@csrf_exempt
def discord_bot_webhook(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("POST")

    if not validate_request(request):
        return HttpResponse('Unauthorized', status=401)

    data_str = request.body.decode()
    data = json.loads(data_str)

    if "type" not in data:
        return HttpResponseBadRequest("No request type could be found")

    return process_discord_bot_webhook(data)

@csrf_exempt
@login_required
def discord_auth_webhook(request):
    state = request.GET.get('state', None)
    if not state:
        return HttpResponseBadRequest("No state parameter")

    stored_state = request.session.pop('oauth2_state', '')
    if state != stored_state:
        return HttpResponseBadRequest("Invalid state parameter")

    code = request.GET.get('code', None)
    if not code:
        return HttpResponseBadRequest("No auth code received")

    authentication_processed = process_discord_auth(request, code)
    if not authentication_processed:
        return HttpResponseServerError("Unable to process request")

    return redirect("user_settings")