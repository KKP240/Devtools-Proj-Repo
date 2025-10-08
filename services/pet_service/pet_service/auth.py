from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.settings import api_settings

class SimpleStatelessUser:
    def __init__(self, user_id, username=None):
        self.id = user_id
        self.username = username or f'user-{user_id}'

    @property
    def is_authenticated(self):
        return True

class StatelessJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return None
        if len(auth) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header')
        token = auth[1].decode('utf-8')

        try:
            UntypedToken(token)
            validated = api_settings.ALGORITHM
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid token')

        from rest_framework_simplejwt.backends import TokenBackend
        backend = TokenBackend(algorithm=api_settings.ALGORITHM, signing_key=api_settings.SIGNING_KEY)
        payload = backend.decode(token, verify=True)
        user_id = payload.get('user_id')
        username = payload.get('username')
        if not user_id:
            raise exceptions.AuthenticationFailed('Token missing user_id')
        return (SimpleStatelessUser(user_id, username), None)
