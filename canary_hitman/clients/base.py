import requests


class BaseClient:
    def __init__(self, base_path: str, token: str) -> None:
        self.token: str = token

        session = requests.Session()
        session.headers = {"Authorization": f"Bearer {token}"}  # type: ignore

        self.session = session
        self.base_path = base_path
