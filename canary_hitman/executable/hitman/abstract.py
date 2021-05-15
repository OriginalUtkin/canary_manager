from abc import ABC

from canary_hitman.executable.hitman.models.result import Result


class AbstractHitman(ABC):
    def hunt(self) -> Result:
        ...
