from canary_hitman.exceptions import HitmanException


class SlackAPIError(HitmanException):
    text: str = "Base exception text"


class ErrorCodeException(SlackAPIError):
    text = "[FAIL] Could not process slack request"


class LookupByEmailException(SlackAPIError):
    text = "[FAIL] User with e-mail {email} doesn't exist"
