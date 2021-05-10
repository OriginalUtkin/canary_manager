from canary_hitman.models.gitlab import Release, Commit
from typing import Optional
from dataclasses import dataclass


@dataclass
class Result:
    deployed_canary_release: Optional[Release]
    current_commit: Commit

    is_deployable: bool
