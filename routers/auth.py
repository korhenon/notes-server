from fastapi import APIRouter

from controller.auth import AuthController
from models.auth_request import SignInRequest, SignUpRequest, SignOutRequest

router = APIRouter(prefix="/auth")


@router.post("/sign-in")
def sign_in(body: SignInRequest):
    return AuthController.sign_in(body)


@router.post("/sign-up")
def sign_up(body: SignUpRequest):
    return AuthController.sign_up(body)


@router.post("/sign-out")
def sign_out(body: SignOutRequest):
    return AuthController.sign_out(body)
