import re
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

from dateutil.parser import parse

from canary_hitman.clients import GitlabClient
from canary_hitman.executable.hitman.abstract import AbstractHitman
from canary_hitman.executable.hitman.kubectl.models import CanaryMeta
from canary_hitman.executable.hitman.models.result import Result
from canary_hitman.models import Commit, CommitterInfo, Release


class HitmanKubectl(AbstractHitman):
    def __init__(
        self, k8s_namespace: str, canary_names: str, commit_to_release_sha: str, project_id: int, gitlab_token: str,
    ) -> None:
        self.k8s_namespace: str = k8s_namespace
        self.canary_names: List[str] = HitmanKubectl.get_pods_to_search(canary_names)
        self.commit_to_release_sha: str = commit_to_release_sha
        self.project_id: int = project_id

        self.gitlab_client = GitlabClient(token=gitlab_token)

    def hunt(self) -> Result:
        canary_meta: Optional[CanaryMeta] = self._get_canary_meta()

        if not canary_meta:
            deployed_canary_release = None
            print(f"Canary pods don't exist for namespace {self.k8s_namespace} and deployments {self.canary_names}")

        else:
            deployed_canary_release = self._get_canary_release(canary_meta)

        current_commit = self._get_commit(repository_id=self.project_id, commit_sha=self.commit_to_release_sha)

        if not current_commit:
            raise Exception()

        return Result(deployed_canary_release, current_commit)

    def _get_canary_meta(self) -> Optional[CanaryMeta]:
        kubectl_output: str = self._run_shell_command(command=f"get pods | grep -E '{'|'.join(self.canary_names)}'")

        if not kubectl_output:
            return None

        canary_pods_meta: List[str] = kubectl_output.strip().split("\n")
        canary_metas: List[CanaryMeta] = list()

        for pod in canary_pods_meta:
            pod_name: str = pod.split()[0]
            described_pod: str = self._run_shell_command(command=f"describe pod {pod_name}")

            commit_sha: str = re.findall(r"Image:\s+[a-z0-9.\/-]+:([a-zA-Z0-9]+)", described_pod)[0]
            deploy_date: datetime = parse(
                re.findall(r"Start\sTime:\s+[a-zA-Z]{3},\s([a-zA-Z0-9,\s:+]+)\n", described_pod)[0]
            ).replace(tzinfo=None)

            canary_metas.append(CanaryMeta(commit_sha, deploy_date))

        if len({r.commit_sha if r else None for r in canary_metas}) > 1:
            raise Exception("Something is wrong in here, couldn't be more than one commit")

        return canary_metas[0]

    def _get_canary_release(self, canary_meta: CanaryMeta) -> Release:
        commit: Optional[Commit] = self._get_commit(repository_id=self.project_id, commit_sha=canary_meta.commit_sha)

        if not commit:
            # Commit that was deployed to canary was squashed or reverted/branch was deleted
            pass

        return Release(deployed_at=canary_meta.deploy_date, commit=commit)

    def _get_commit(self, repository_id: int, commit_sha: str) -> Optional[Commit]:
        api_commit: Dict = self.gitlab_client.request_api(
            path=f"/projects/{repository_id}/repository/commits/{commit_sha}"
        )

        if not api_commit:
            return None

        return Commit(
            sha=commit_sha,
            web_link=api_commit["web_url"],
            committer=CommitterInfo(email=api_commit["committer_email"]),
        )

    def _run_shell_command(self, command: str) -> str:
        try:
            return subprocess.check_output(f"kubectl -n {self.k8s_namespace} {command}", shell=True).decode("utf-8")
        except subprocess.CalledProcessError as e:
            if not e.output:
                return ""
            raise RuntimeError(f"command return with error (code {e.returncode}): {e.output}")

    @staticmethod
    def get_pods_to_search(canary_names: str) -> List[str]:
        return list(map(lambda pod_name: pod_name + "-*", canary_names.split(",")))
