from abc import ABC, abstractmethod
from .advisor import advise

class AdvisingStrategy(ABC):
    """
    Abstract base class defining the interface for advising strategies.
    All concrete advising strategies should inherit from this class.
    """
    
    @abstractmethod
    def advise_solution(self, services: dict, model_id=None) -> dict:
        pass


class GPTAdvisingStrategy(AdvisingStrategy):
    """
    Concrete implementation of AdvisingStrategy that uses GPT to provide workflow advice.
    """
    
    def __init__(self, model="gpt-4"):
        self.model = model
    
    def advise_solution(self, services: dict, model_id) -> dict:
        """
        Uses GPT to analyze workflow data and provide optimization advice.
        """
        return advise(services, model_id)