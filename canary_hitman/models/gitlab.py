from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CommitterInfo:
    email: str


@dataclass
class Commit:
    sha: str
    web_link: str
    committer: CommitterInfo


@dataclass
class Release:
    deployed_at: datetime
    commit: Optional[Commit]
