"""Account and sign-in requests and responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    # A plain string, not EmailStr: a malformed address must get the same 401 as a wrong password
    # (BR3), not a 400 that tells the caller the address was the problem.
    email: str = Field(max_length=254)
    password: str = Field(max_length=128)


class RegisterRequest(BaseModel):
    # Plain strings: the service checks the address and the password length itself, so the answer
    # is the exact sentence of US01 with its code, not FastAPI's generic validation text. The
    # limits below only stop an absurdly long request before it is hashed.
    email: str = Field(max_length=254)
    password: str = Field(max_length=1024)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserOut
