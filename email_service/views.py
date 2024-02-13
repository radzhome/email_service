import json
import logging
from urllib.parse import urlparse


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from email_service.utils import send_gmail

ALLOWED_USER_AGENTS = settings.ALLOWED_USER_AGENTS
ORIGIN_TO_EMAIL = settings.ORIGIN_TO_EMAIL

@csrf_exempt  # Only use csrf_exempt for demonstration purposes, consider using CSRF protection in production.
@require_POST
def post_email(request):
    user_agent = request.headers.get('User-Agent', '')

    origin = request.headers.get('Origin')
    if origin in settings.CORS_ALLOWED_ORIGINS and any(agent in user_agent for agent in ALLOWED_USER_AGENTS):
        message = request.POST.get('message')
        from_user = request.POST.get('from_user', '')
        subject = request.POST.get('subject', f'A message from a user {from_user} on {origin}')

        from_user_email = request.POST.get('from_user_email')

        if not (from_user_email and message):
            try:
                data = json.loads(request.body)
                from_user = data.get('from_user', '')
                from_user_email = data.get('from_user_email', '')
                subject = data.get('subject', f'A message from a user {from_user} on {origin}')
                message = data.get('message', '')
            except json.JSONDecodeError:
                # No JSON in the request body
                logging.error("view.post_email: Invalid request. request.body=%s...", request.body[:200])
                return HttpResponse("Invalid request", status=400)

        # Modify the message to include the reply-to information
        # reply_to = from_user_email  # Set the reply-to address

        # Send the email
        parsed_origin = urlparse(origin)
        origin_domain = parsed_origin.netloc
        send_to = ORIGIN_TO_EMAIL.get(origin_domain, {}).get('to-emails')
        send_gmail(subject=subject, message=message, reply_to=from_user_email, send_to=send_to)

        # Do something with from_user and message
        return HttpResponse("Done!")

    else:
        parsed_origin = urlparse(origin)
        origin_domain = parsed_origin.netloc

        # Just respond 404 instead of 400 or 403 if the request is not allowed
        logging.error("view.post_email: Not found. origin=%s, origin_domain=%s, user_agent=%s", origin, origin_domain, user_agent)
        return HttpResponse("Not found", status=404)


def health(request):
    return HttpResponse("Pong")

