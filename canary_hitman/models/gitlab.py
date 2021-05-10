from dataclasses import dataclass
from datetime import datetime


@dataclass
class CommitterInfo:
    name: str
    email: str


@dataclass
class Commit:
    sha: str
    web_link: str
    committer: CommitterInfo


@dataclass
class Release:
    deployed_at: datetime
    commit: Commit
