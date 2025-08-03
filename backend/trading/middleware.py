from django.conf import settings
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
                
                timeout_period = timedelta(seconds=settings.SESSION_TIMEOUT)
                
                if timezone.now() - last_activity > timeout_period:
                    logout(request)
                    messages.warning(request, 'You have been automatically logged out due to inactivity.')
                    return redirect('home')
            
            request.session['last_activity'] = timezone.now().isoformat()
        
        response = self.get_response(request)
        return response 