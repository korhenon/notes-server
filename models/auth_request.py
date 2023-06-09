from pydantic import BaseModel


class SignInRequest(BaseModel):
    email: str
    password: str


class SignUpRequest(BaseModel):
    name: str
    email: str
    password: str


class SignOutRequest(BaseModel):
    token: str
