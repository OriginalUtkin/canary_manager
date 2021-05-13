import json
from typing import Dict, Optional

from canary_hitman.clients.base import BaseClient


class GitlabClient(BaseClient):
    def request_api(self, path: str, params: Optional[Dict] = None) -> Dict:

        if not params:
            params = {}

        response = self.session.get("https://gitlab.skypicker.com/api/v4" + path, params=params,)

        response.raise_for_status()

        return json.loads(response.text)
