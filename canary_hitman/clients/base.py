import requests


class BaseClient:
    def __init__(self, token: str) -> None:
        self.token: str = token

        session = requests.Session()
        session.headers = {"Authorization": f"Bearer {token}"}  # type: ignore

        self.session = session
