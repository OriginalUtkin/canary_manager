from datetime import datetime

import pytest

from canary_hitman.executable.hitman.kubectl.executor import Executor
from canary_hitman.executable.hitman.kubectl.models import CanaryMeta
from canary_hitman.models.gitlab import Commit, CommitterInfo, Release


@pytest.mark.vcr
@pytest.mark.parametrize(
    "canary_meta_commit_sha, expected_result",
    [
        (
            pytest.param(
                "c8f76d8f4e1b361ddcaf6086f70d9bb5e44487ab",
                Release(
                    deployed_at=datetime(2021, 5, 14, 12, 49, 27),
                    commit=Commit(
                        sha="c8f76d8f4e1b361ddcaf6086f70d9bb5e44487ab",
                        web_link="https://gitlab.com/path",
                        committer=CommitterInfo(email="email@email.com"),
                    ),
                ),
                id="existing_commit_sha",
            )
        ),
        (
            pytest.param(
                "dummy_commit_sha",
                Release(deployed_at=datetime(2021, 5, 14, 12, 49, 27), commit=None),
                id="not_existing_commit_sha",
            )
        ),
    ],
)
def test_built_release(dummy_kubectl_executor: Executor, canary_meta_commit_sha: str, expected_result: Release) -> None:
    canary_meta = CanaryMeta(commit_sha=canary_meta_commit_sha, deploy_date=datetime(2021, 5, 14, 12, 49, 27))

    result = dummy_kubectl_executor._get_canary_release(canary_meta=canary_meta)

    assert expected_result == result
