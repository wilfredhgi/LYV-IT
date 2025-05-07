import datetime
from django.conf import settings
from django.contrib.sessions.models import Session


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_timeout = getattr(settings, 'SESSION_IDLE_TIMEOUT', 1800)  # Default: 30 minutes
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = datetime.datetime.now().timestamp()

            if last_activity and now - last_activity > session_timeout:
                # Logout the user or clear session
                request.session.flush()  # Clears the session.
            else:
                request.session['last_activity'] = now

        response = self.get_response(request)
        return response
