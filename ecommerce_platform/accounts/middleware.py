from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect
from datetime import timedelta


class UpdateLastActivityMiddleware:
    """
    Middleware to track and update user's last activity timestamp.
    Updates the last_active_datetime field whenever an authenticated user makes a request.
    """
    def __init__(self, get_response):
        """  Initialize the middleware. """
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        """ Process the request and update user's last activity time. """
        response = self.get_response(request)
        if request.user.is_authenticated:
            get_user_model().objects.filter(pk=request.user.pk).update(
                last_active_datetime=timezone.now()
            )

        return response


class SessionTimeoutMiddleware:
    """
    Middleware to handle session timeout based on user inactivity.
    Logs out users who have been inactive for longer than the session timeout period.
    """
    def __init__(self, get_response):
        """
        Initialize the middleware with a default session timeout of 60 seconds.
        """
        self.get_response = get_response
        self.session_timeout = 60

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """ Process the request and check for session timeout. """
        if request.user.is_authenticated:
            last_activity_time = request.user.last_active_datetime
            inactivity_duration = timezone.now() - last_activity_time
            if inactivity_duration.total_seconds() > self.session_timeout:
                logout(request)
                messages.warning(request, "Your session has expired due to inactivity. Sign in again.")
                request.session.flush()
                return redirect('accounts:login')

        response = self.get_response(request)
        return response
