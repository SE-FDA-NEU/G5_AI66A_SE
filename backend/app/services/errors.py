"""The ways a service can refuse a request.

A service raises one of these with the exact sentence the user should read and a short `code`
that names it. The service never says which HTTP status that is: app/core/errors.py maps each
kind to its status, once, for the whole API (docs/design.md, section 3).
"""


class ServiceError(Exception):
    """A refusal the user can act on. The app chooses its message by `code`, not by the text."""

    code = "refused"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code


class NotUnderstood(ServiceError):
    """The request is malformed, such as an address with no @ or a month written 11/2026."""

    code = "invalid_request"


class NotSignedIn(ServiceError):
    """Nobody is signed in, or the details given do not open an account (BR3, BR10)."""

    code = "sign_in_again"


class AlreadyExists(ServiceError):
    """The request conflicts with what is stored, such as an address already registered (BR1)."""

    code = "conflict"


class RuleBroken(ServiceError):
    """A well-formed request that breaks a business rule (BR2, BR5, BR6, BR11)."""

    code = "rule_broken"
