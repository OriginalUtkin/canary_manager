#!/usr/bin/python
from canary_hitman.clients.slack.exceptions import SlackAPIError
from canary_hitman.executable.hitman.hitman import Hitman, Result
from canary_hitman.executable.notifier.notifier import Notifier
from canary_hitman.utils import (
    MissingVariableException,
    get_environ_var,
    handle_exception,
)

if __name__ == "__main__":
    with handle_exception(MissingVariableException):
        canary_names: str = get_environ_var("PODS")
        ttl: int = int(get_environ_var("CANARY_TTL"))
        k8s_namespace: str = get_environ_var("K8S_NAMESPACE")
        commit_to_release_sha: str = get_environ_var("COMMIT_SHA")
        project_id: str = get_environ_var("PROJECT_ID")
        gitlab_token: str = get_environ_var("GITLAB_API_TOKEN")

        channel_to_notify: str = get_environ_var("CHANNEL_TO_NOTIFY")
        slack_token: str = get_environ_var("SLACK_TOKEN")

        repository_name: str = get_environ_var("REPOSITORY_NAME")

    hitman = Hitman(
        canary_names=canary_names,
        ttl=int(ttl),
        k8s_namespace=k8s_namespace,
        commit_to_release_sha=commit_to_release_sha,
        project_id=int(project_id),
        gitlab_token=gitlab_token,
    )

    hunt_result: Result = hitman.hunt()

    with handle_exception(custom_exception=SlackAPIError):
        notifier = Notifier(channel_to_notify=channel_to_notify, slack_token=slack_token,)

    if not hunt_result.deployed_canary_release:
        notifier.notify_new_release(
            canary_releaser_email=hunt_result.current_commit.committer.email,
            new_canary_commit_link=hunt_result.current_commit.web_link,
            project_name=repository_name,
        )

        exit(0)

    if hunt_result.is_deployable:
        notifier.notify_override(
            canary_releaser_email=hunt_result.current_commit.committer.email,
            previous_canary_releaser_email=hunt_result.deployed_canary_release.commit.committer.email,
            new_canary_commit_link=hunt_result.current_commit.web_link,
            project_name=repository_name,
        )

        exit(0)

    exit(1)
