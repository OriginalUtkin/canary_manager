from dataclasses import dataclass
from typing import Optional

from canary_hitman.models.gitlab import Commit, Release


@dataclass
class Result:
    deployed_canary_release: Optional[Release]
    current_commit: Commit
