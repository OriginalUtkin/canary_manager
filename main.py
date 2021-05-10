#!/usr/bin/python
from canary_hitman.executable.hitman.hitman import Hitman, Result
from canary_hitman.executable.notifier.notifier import Notifier
import os


CANARY_POSTFIX = "canary"

if __name__ == '__main__':
    repository_name: str = os.getenv("REPOSITORY_NAME")

    hitman = Hitman(
        canary_names=os.getenv("PODS"),
        ttl=os.getenv("CANARY_TTL"),
        k8s_namespace=os.getenv("K8S_NAMESPACE"),
        repository_name=repository_name,
        commit_to_release_sha=os.getenv("COMMIT_SHA")
    )

    hunt_result: Result = hitman.hunt()

    notifier = Notifier(channel_to_notify=os.getenv("CHANNEL_TO_NOTIFY"), slack_token=os.getenv("SLACK_TOKEN"))

    if not hunt_result.deployed_canary_release:
        notifier.notify_new_release(
            canary_releaser_email=hunt_result.current_commit.committer.email,
            new_canary_commit_link=hunt_result.current_commit.web_link,
            project_name=repository_name
        )

        exit(0)

    if hunt_result.is_deployable:
        notifier.notify_override(
            canary_releaser_email=hunt_result.current_commit.committer.email,
            previous_canary_releaser_email=hunt_result.deployed_canary_release.commit.committer.email,
            new_canary_commit_link=hunt_result.current_commit.web_link,
            project_name=repository_name
        )

        exit(0)

    exit(1)
