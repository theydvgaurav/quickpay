import os

import jwt.exceptions
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import action

from base.views import ApplicationBaseViewSet
from exceptions import APIException
from users.models import User
from users.serializer import RegisterUserSerializer, LoginUserSerializer
from utils.generate_jwt import generate_access_refresh_token, decode_jwt


class UserViewSet(ApplicationBaseViewSet):
    action_to_request_serializer_class = {
        'register': RegisterUserSerializer,
        'login': LoginUserSerializer
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @action(methods=['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        sz = self.get_request_serializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            data = sz.data
            existing_user = User.objects.filter(email=data.get('email'))
            if existing_user:
                raise APIException('User with same email already exists', 400)
            hashed_password = make_password(data.get('password'))
            user = User(email=data.get('email'), name=data.get('name'), password=hashed_password)
            user.save()
            access_token, refresh_token, access_token_exp = generate_access_refresh_token(
                {"userId": str(user.user_id), "name": user.name},
                os.getenv("JWT_ADMIN_ENCODE_SECRET"))
            return self.get_response(data={"accessToken": access_token, "refreshToken": refresh_token,
                                           "accessTokenExp": int(access_token_exp)})

    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        sz = self.get_request_serializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            data = sz.data
            try:
                user = User.objects.get(email=data.get('email'))
            except Exception as e:
                raise APIException('Invalid Credentials', 401)
            if check_password(data.get('password'), user.password):
                access_token, refresh_token, access_token_exp = generate_access_refresh_token(
                    {"userId": str(user.user_id), "name": user.name},
                    os.getenv("JWT_ADMIN_ENCODE_SECRET"))
                return self.get_response(data={"accessToken": access_token, "refreshToken": refresh_token,
                                               "accessTokenExp": int(access_token_exp)})

    @action(methods=["POST"], detail=False, url_path="refresh-token")
    def refresh_token(self, request):
        """"""
        refresh_token_header = get_authorization_header(request)
        refresh_token = refresh_token_header.decode().split("Bearer ")[-1]
        access_token = None
        scope = None
        try:
            payload = decode_jwt(refresh_token, os.getenv("JWT_ADMIN_ENCODE_SECRET"))
            if not payload:
                raise
            if payload.get("tokenType") != "REFRESH":
                raise APIException("INVALID_TOKEN_TYPE", 401)
            access_token, _, access_token_exp = generate_access_refresh_token(
                {"userId": payload.get("userId"), "name": payload.get("name")},
                os.getenv("JWT_ADMIN_ENCODE_SECRET"))
        except APIException:
            raise
        except jwt.exceptions.ExpiredSignatureError:
            raise APIException("REFRESH_TOKEN_EXPIRED", 401)
        except Exception as exp:
            raise APIException("INVALID_REFRESH_TOKEN", 401)
        return self.get_response(data={
            "accessToken": access_token,
            "accessTokenExp": int(access_token_exp)
        })
