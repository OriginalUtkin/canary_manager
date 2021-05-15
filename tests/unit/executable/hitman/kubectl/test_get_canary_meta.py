import subprocess
from datetime import datetime
from typing import List, Optional

import pytest

from canary_hitman.executable.hitman.kubectl import CanaryMeta
from canary_hitman.executable.hitman.kubectl.executor import Executor
from tests.shell_commands_outputs import described_pod, pods


@pytest.mark.parametrize(
    "check_output_return_values, expected_result",
    [
        pytest.param(
            [pods, described_pod],
            CanaryMeta(
                commit_sha="c8f76d8f4e1b361ddcaf6086f70d9bb5e44487ab", deploy_date=datetime(2021, 5, 14, 12, 49, 27)
            ),
            id="existing_pods",
        ),
        pytest.param([b""], None, id="not_existing_pods"),
    ],
)
def test_get_canary_meta(
    mocker,
    dummy_kubectl_executor: Executor,
    check_output_return_values: List[str],
    expected_result: Optional[CanaryMeta],
) -> None:

    mocker.patch.object(subprocess, "check_output", side_effect=check_output_return_values, autospec=True)

    meta = dummy_kubectl_executor._get_canary_meta()

    assert meta == expected_result
