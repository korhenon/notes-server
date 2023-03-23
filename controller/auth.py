import datetime

import jwt

import config
from database.models import User
from models.auth_request import SignUpRequest, SignInRequest, SignOutRequest
from models.auth_response import SignInAndUpResponse, SignOutResponse
from dataclasses import dataclass


@dataclass
class TokenPayload:
    email: str
    iss: str


class AuthController:
    @staticmethod
    def sign_up(body: SignUpRequest) -> SignInAndUpResponse:
        if not AuthController.is_user_exists(body.email):
            new_user = User(name=body.name, email=body.email, password=body.password)
            token = AuthController.generate_token(body.email)
            new_user.token = token
            new_user.save()
            return SignInAndUpResponse(token=token)
        return SignInAndUpResponse(error="User with this email already exists!")

    @staticmethod
    def sign_in(body: SignInRequest) -> SignInAndUpResponse:
        if not AuthController.is_user_exists(body.email):
            return SignInAndUpResponse(error="User doesn't exists!")
        user = User.get(User.email == body.email)
        if user.password != body.password:
            return SignInAndUpResponse(error="Password doesn't right!")
        token = AuthController.generate_token(body.email)
        user.token = token
        user.save()
        return SignInAndUpResponse(token=token)

    @staticmethod
    def sign_out(body: SignOutRequest) -> SignOutResponse:
        if AuthController.can_authenticate(body.token):
            user = AuthController.authenticate(body.token)
            user.token = None
            user.save()
            return SignOutResponse()
        return SignOutResponse(successful=False)

    @staticmethod
    def is_user_exists(email: str) -> bool:
        return len(User.select().where(User.email == email)) != 0

    @staticmethod
    def can_authenticate(token: str):
        email = AuthController.read_token(token).email
        is_exists = AuthController.is_user_exists(email)
        if is_exists:
            return User.get(User.email == email).token == token
        return False

    @staticmethod
    def authenticate(token: str) -> User:
        return User.get(User.email == AuthController.read_token(token).email)

    @staticmethod
    def generate_token(email: str) -> str:
        return jwt.encode({
            "email": email,
            "iss": str(datetime.datetime.now())
        }, config.JWT_SECRET, algorithm="HS256")

    @staticmethod
    def read_token(token: str) -> TokenPayload:
        decoding = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        return TokenPayload(email=decoding["email"], iss=decoding["iss"])
