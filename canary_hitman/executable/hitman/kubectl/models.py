from dataclasses import dataclass
from datetime import datetime


@dataclass
class CanaryMeta:
    commit_sha: str
    deploy_date: datetime
