import json
from typing import Dict, Optional

from requests.exceptions import HTTPError

from canary_hitman.clients.base import BaseClient
from canary_hitman.models import Commit, CommitterInfo


class GitlabClient(BaseClient):
    def request_api(self, path: str, params: Optional[Dict] = None) -> Dict:

        if not params:
            params = {}

        response = self.session.get("https://gitlab.skypicker.com/api/v4" + path, params=params,)

        response.raise_for_status()

        return json.loads(response.text)

    def get_commit(self, repository_id: int, commit_sha: str) -> Optional[Commit]:
        try:
            api_commit: Dict = self.request_api(path=f"/projects/{repository_id}/repository/commits/{commit_sha}")

        except HTTPError as e:
            if e.response.status_code == 404:
                return None
            else:
                raise

        return Commit(
            sha=commit_sha,
            web_link=api_commit["web_url"],
            committer=CommitterInfo(email=api_commit["committer_email"]),
        )
