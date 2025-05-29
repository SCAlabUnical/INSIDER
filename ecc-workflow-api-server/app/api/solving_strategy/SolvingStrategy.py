from abc import ABC, abstractmethod
from .utils import log_method_call


class SolvingStrategy(ABC):
    @log_method_call
    @abstractmethod
    def solve(self, workflow: dict, catalog: dict) -> dict:
        pass