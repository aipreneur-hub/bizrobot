from abc import ABC, abstractmethod

class Adapter(ABC):
    @abstractmethod
    async def execute(self, step: dict, ctx: dict) -> dict: ...
