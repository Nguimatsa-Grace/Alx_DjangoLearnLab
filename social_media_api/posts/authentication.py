# posts/authentication.py

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class QueryParamTokenAuthentication(TokenAuthentication):
    """
    Custom authentication class that first looks for the token in the 
    URL query parameters (e.g., ?token=...) and falls back to the 
    Authorization header if not found.
    """
    def authenticate(self, request):
        # 1. Check query parameters for the 'token' key
        token_key = request.query_params.get('token')
        
        if token_key:
            # If the token is found in the URL, authenticate it
            return self.authenticate_credentials(token_key)
        
        # 2. If no token in query params, fall back to default header check
        return super().authenticate(request)