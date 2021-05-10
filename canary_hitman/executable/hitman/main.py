#!/usr/bin/python
import os
from .hitman import Hitman, Result

if __name__ == "__main__":
    hitman = Hitman(
        canary_names=os.getenv("CANARY_POSTFIX"),
        ttl=os.getenv("CANARY_TTL"),
        k8s_namespace=os.getenv("NAMESPACE"),
        repository_name=os.getenv("REPOSITORY_NAME"),
        commit_to_release_sha=os.getenv("COMMIT_SHA")
    )

    hunt_result: Result = hitman.hunt()

    if hunt_result.is_deployable:
        exit(0)

    exit(1)
