import re
import subprocess
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from dateutil.parser import parse

from canary_hitman.clients import GitlabClient
from canary_hitman.models import Commit, CommitterInfo, Release

from .models.result import Result


class Hitman:
    def __init__(
        self, k8s_namespace: str, canary_names: str, ttl: int, repository_name: str, commit_to_release_sha: str,
    ) -> None:
        self.k8s_namespace: str = k8s_namespace
        self.canary_names: List[str] = Hitman.get_pods_to_search(canary_names)
        self.canary_ttl: int = ttl
        self.repository_name: str = repository_name
        self.commit_to_release_sha: str = commit_to_release_sha

        self.gitlab_client = GitlabClient()

    def hunt(self) -> Result:
        get_pods_output: str = self._run_shell_command(command=f"get pods | grep -E '{'|'.join(self.canary_names)}'")
        canary_pods: List[str] = get_pods_output.strip().split("\n")

        if not canary_pods:
            print(f"Canary pods don't exist for namespace {self.k8s_namespace} and deployments {self.canary_names}")
            deployed_canary_release: Optional[Release] = None

        else:
            # TODO: If release is not exist but pods are found -> deployed commit was squashed/branch was deleted --> HOW to handle?
            deployed_canary_release = self._build_release(pods=canary_pods)

        current_commit = self._get_commit(repository_id="333", commit_sha=self.commit_to_release_sha)

        if not current_commit:
            raise Exception()

        return Result(
            deployed_canary_release,
            current_commit,
            is_deployable=not deployed_canary_release
            or self._is_ttl_expired(deployed_at=deployed_canary_release.deployed_at),
        )

    def _build_release(self, pods: List) -> Release:
        # TODO: Move it to hunt method
        repositories: Dict = self.gitlab_client.request_api(path="/projects", params={"search": self.repository_name})
        # TODO: get repository id using gitlab API
        repository_id = "333"

        releases: List[Release] = list()

        for pod in pods:
            pod_name: str = pod.split()[0]
            described_pod: str = self._run_shell_command(command=f"describe pod {pod_name}")

            commit_sha: str = re.findall(r"Image:\s+[a-z0-9.\/-]+:([a-zA-Z0-9]+)", described_pod)[0]
            deploy_date: datetime = parse(
                re.findall(r"Start\sTime:\s+[a-zA-Z]{3},\s([a-zA-Z0-9,\s:+]+)\n", described_pod)[0]
            ).replace(tzinfo=None)

            commit: Optional[Commit] = self._get_commit(repository_id=repository_id, commit_sha=commit_sha)

            if not commit:
                # Commit that was deployed to canary was squashed or reverted/branch was deleted
                continue

            releases.append(Release(deployed_at=deploy_date, commit=commit))

        if len({r.commit.sha if r else None for r in releases}) > 1:
            raise Exception("Something is wrong in here, couldn't be more than one commit")

        return releases[0]

    def _get_commit(self, repository_id: str, commit_sha: str) -> Optional[Commit]:
        api_commit: Dict = self.gitlab_client.request_api(
            path=f"/projects/{repository_id}/repository/commits/{commit_sha}"
        )

        if not api_commit:
            return None

        return Commit(
            sha=commit_sha,
            web_link=api_commit["web_url"],
            committer=CommitterInfo(name=api_commit["committer_name"], email=api_commit["committer_email"]),
        )

    def _is_ttl_expired(self, deployed_at: datetime) -> bool:
        return datetime.now() - deployed_at >= timedelta(hours=self.canary_ttl)

    def _run_shell_command(self, command: str) -> str:
        return subprocess.check_output(["/bin/bash", "-c", f"kubectl -n {self.k8s_namespace} {command}"]).decode(
            "utf-8"
        )

    @staticmethod
    def get_pods_to_search(canary_names: str) -> List[str]:
        return list(map(lambda pod_name: pod_name + "-*", canary_names.split(",")))
