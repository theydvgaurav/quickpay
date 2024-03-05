import os
import re

from rest_framework import authentication
from rest_framework.authentication import get_authorization_header

from exceptions import APIException
from users.models import User
from utils.generate_jwt import decode_jwt

IGNORE_PATH_PATTERN = [
    r"\/v1\/users\/login\/",
    r"\/v1\/users\/register\/",
    r"\/v1\/users\/refresh-token\/"
]


class QuickPayUserAuthentication(authentication.BaseAuthentication):
    def __init__(self, **kwargs):
        """"""
        super().__init__(**kwargs)

    def authenticate(self, request):
        user, val, shall_ignore = self.ignore_auth_header(request.path, request.method)
        if shall_ignore:
            return user, val
        auth_token_header = get_authorization_header(request)
        if not auth_token_header:
            raise APIException("MISSING_HEADER_TOKEN", 401)
        auth_token = auth_token_header.decode().split("Bearer ")[-1]
        try:
            payload = decode_jwt(auth_token, os.getenv("JWT_ADMIN_ENCODE_SECRET"))
            if payload.get("tokenType") != "ACCESS":
                raise APIException("INVALID_TOKEN_TYPE", 401)
            user = User.objects.get(user_id=payload.get('userId'))
        except Exception as e:
            raise APIException("INVALID_TOKEN", 401)
        return user, None

    @staticmethod
    def ignore_auth_header(path, method):
        """"""
        for item in IGNORE_PATH_PATTERN:
            if re.match(item, path):
                print("IGNORING_AUTH")
                return None, None, True
        return None, None, False
