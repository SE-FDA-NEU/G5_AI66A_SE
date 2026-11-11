"""The profile and the account, as /api/users/me receives them (US16, US18)."""

from pydantic import BaseModel, ConfigDict, Field


class ProfileUpdate(BaseModel):
    """Only the fields sent change; an empty string clears one (BR15).

    `email` is not a field: a request that sends it is refused as malformed, because the address
    an account was created with never changes. The limits here only stop an absurd request; the
    service checks the real ones and answers with the sentence the app shows.
    """

    model_config = ConfigDict(extra="forbid")

    full_name: str | None = Field(default=None, max_length=1000)
    nickname: str | None = Field(default=None, max_length=1000)
    phone: str | None = Field(default=None, max_length=1000)
    # A data: URL; about 270,000 characters for the largest picture BR15 allows.
    avatar: str | None = Field(default=None, max_length=400_000)


class AccountDeletion(BaseModel):
    """BR16: the email and the current password, asked again before the account is deleted."""

    email: str = Field(max_length=254)
    password: str = Field(max_length=1024)
