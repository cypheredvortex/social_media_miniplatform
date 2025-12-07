from django.utils.deprecation import MiddlewareMixin
from .auth_backends import MongoDBAuthBackend

class SessionAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check our custom session first
        user_id = request.session.get('user_id')
        if user_id:
            backend = MongoDBAuthBackend()
            user = backend.get_user(user_id)
            if user:
                request.user = user
                return None
        
        # If not in our session, check Django's auth
        from django.contrib.auth import get_user
        user = get_user(request)
        if user.is_authenticated:
            request.user = user
        
        return None
    
    def process_response(self, request, response):
        return response