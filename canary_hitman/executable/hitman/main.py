#!/usr/bin/python
from canary_hitman.utils import get_environ_var

from .hitman import Hitman, Result

if __name__ == "__main__":
    hitman = Hitman(
        canary_names=get_environ_var("CANARY_POSTFIX"),
        ttl=int(get_environ_var("CANARY_TTL")),
        k8s_namespace=get_environ_var("NAMESPACE"),
        commit_to_release_sha=get_environ_var("COMMIT_SHA"),
        project_id=int(get_environ_var("PROJECT_ID")),
        gitlab_token=get_environ_var("GITLAB_API_TOKEN"),
    )

    hunt_result: Result = hitman.hunt()

    if hunt_result.is_deployable:
        exit(0)

    exit(1)
