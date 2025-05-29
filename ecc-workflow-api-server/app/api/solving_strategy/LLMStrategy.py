from .gptsolver import solver
from .SolvingStrategy import SolvingStrategy
from .utils import log_method_call

class LLMStrategy (SolvingStrategy):
    @log_method_call
    def __init__(self):
        pass
    
    @log_method_call
    def solve(self, workflow: dict, catalog: dict, model: int) -> dict:
        return {
            'message': 'Workflow and catalog successfully received',
            'result': solver.solve(workflow=workflow, catalog=catalog, model_choice=model)
        }