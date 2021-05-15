from typing import Any, Dict

import pytest

from canary_hitman import Executor


@pytest.fixture
def vcr_config() -> Dict[str, Any]:
    return {"filter_headers": [("authorization", "Bearer Token Value")], "record_mode": "none"}


@pytest.fixture
def dummy_kubectl_executor() -> Executor:
    return Executor(
        k8s_namespace="dummy", canary_names="dummy", commit_to_release_sha="dummy", project_id=0, gitlab_token="dummy"
    )
