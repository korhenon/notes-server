from typing import Union
from pydantic import BaseModel


class SignInAndUpResponse(BaseModel):
    token: Union[str, None] = None
    error: Union[str, None] = None


class SignOutResponse(BaseModel):
    successful: bool = True
