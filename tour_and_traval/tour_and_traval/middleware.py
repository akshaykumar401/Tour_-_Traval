from django.shortcuts import redirect
from django.conf import settings

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            restricted_paths = [
                '/accounts/login/',
                '/accounts/password_reset/',
                '/accounts/reset/',
            ]
            
            # If the requested path starts with any of the restricted paths, redirect
            if any(request.path.startswith(path) for path in restricted_paths):
                # Redirect to the user page or LOGIN_REDIRECT_URL
                return redirect('user_page')
                
        response = self.get_response(request)
        return response
