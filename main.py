#!/usr/bin/python
from canary_hitman.executable.hitman.hitman import Hitman, Result
from canary_hitman.executable.notifier.notifier import Notifier
from canary_hitman.utils import get_environ_var

if __name__ == "__main__":
    repository_name: str = get_environ_var("REPOSITORY_NAME")
    canary_names: str = get_environ_var("PODS")
    ttl: int = int(get_environ_var("CANARY_TTL"))
    k8s_namespace: str = get_environ_var("K8S_NAMESPACE")
    commit_to_release_sha: str = get_environ_var("COMMIT_SHA")
    project_id: str = get_environ_var("PROJECT_ID")

    hitman = Hitman(
        canary_names=canary_names,
        ttl=int(ttl),
        k8s_namespace=k8s_namespace,
        commit_to_release_sha=commit_to_release_sha,
        project_id=int(project_id),
    )

    hunt_result: Result = hitman.hunt()

    notifier = Notifier(
        channel_to_notify=get_environ_var("CHANNEL_TO_NOTIFY"), slack_token=get_environ_var("SLACK_TOKEN"),
    )

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
