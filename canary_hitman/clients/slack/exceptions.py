from canary_hitman.exceptions import HitmanException


class SlackAPIError(HitmanException):
    text: str = "Base exception text"


class ErrorCodeException(SlackAPIError):
    def __init__(self, reason: str) -> None:
        self.text = f"[FAIL] Could not process slack request. Reason: {reason}"


class LookupByEmailException(SlackAPIError):
    def __init__(self, email: str) -> None:
        self.text = f"[FAIL] User with e-mail {email} doesn't exist"
