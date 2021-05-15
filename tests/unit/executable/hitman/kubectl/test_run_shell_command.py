import subprocess

import pytest

from canary_hitman import Executor

executed_command: str = "get_pods"


def test_run_shell_command(mocker, dummy_kubectl_executor: Executor) -> None:
    mocker.patch.object(
        subprocess,
        "check_output",
        return_value="some output",
        side_effect=subprocess.CalledProcessError(returncode=1, cmd=executed_command, output=""),
        autospec=True,
    )

    result = dummy_kubectl_executor._run_kubectl_command(executed_command)

    assert result == ""


def test_run_shell_command_exception(mocker, dummy_kubectl_executor: Executor) -> None:
    mocker.patch.object(
        subprocess,
        "check_output",
        return_value="some output",
        side_effect=subprocess.CalledProcessError(returncode=1, cmd=executed_command, output="Exception Traceback"),
        autospec=True,
    )

    with pytest.raises(RuntimeError):
        dummy_kubectl_executor._run_kubectl_command(executed_command)
