import json
from typing import Dict, Optional, Union, List

from requests.exceptions import HTTPError

from canary_hitman.clients.base import BaseClient
from canary_hitman.models import Commit, CommitterInfo


class GitlabClient(BaseClient):
    def request_api_get(self, path: str, params: Optional[Dict] = None, json_output: bool = True) -> Union[List, Dict]:

        if not params:
            params = {}

        response = self.session.get(self.base_path + path, params=params,)

        response.raise_for_status()

        if json_output:
            return json.loads(response.text)

        else:
            return response.text

    def create_merge_request(
        self,
        repository_id: Union[str, int],
        source_branch: str,
        target_branch: str,
        title: str,
    ):
        response = self.session.post(
            f"{self.base_path}/projects/{repository_id}/merge_requests", json={
                "source_branch": source_branch,
                "target_branch": target_branch,
                "title": title,
            },
        )

        response.raise_for_status()

        return json.loads(response.text)

    def update_file(self, project_id: Union[int, str], branch: str, message: str, file_name: str, file_content: str):
        response = self.session.post(
            f"{self.base_path}/projects/{project_id}/repository/commits", json={
                "branch": branch,
                "commit_message": message,
                "actions": [{"action": "update", "file_path": f"{file_name}", "content": f"{file_content}"}]
            },
        )

        response.raise_for_status()

        return json.loads(response.text)

    def get_commit(self, repository_id: int, commit_sha: str) -> Optional[Commit]:
        try:
            api_commit: Dict = self.request_api_get(path=f"/projects/{repository_id}/repository/commits/{commit_sha}")

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

    def create_branch(self, project_id: int, branch: str, ref: str):
        self.session.post(
            f"{self.base_path}/projects/{project_id}/repository/branches",
            params={
                "branch": branch,
                "ref": ref
            }
        )

