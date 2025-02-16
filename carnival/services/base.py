from abc import ABC
from typing import Optional


class Service(ABC):
    """abstract base service that all services should inherit from"""

    name: Optional[str] = None
    ready: bool = True

    async def teardown(self) -> None:
        return

    def set_ready(self, val: bool = True) -> None:
        self.ready = val
