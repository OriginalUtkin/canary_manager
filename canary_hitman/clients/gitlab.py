import json
import os
from typing import Dict, Optional

import requests


class GitlabClient:
    def __init__(self) -> None:
        self.git_token = os.getenv("GITLAB_API_TOKEN")

    def request_api(self, path: str, params: Optional[Dict] = None) -> Dict:

        if not params:
            params = {}

        response = requests.get(
            "https://gitlab.skypicker.com/api/v4" + path,
            params=params,
            headers={"Authorization": f"Bearer {self.git_token}"},
        )

        response.raise_for_status()

        return json.loads(response.text)
