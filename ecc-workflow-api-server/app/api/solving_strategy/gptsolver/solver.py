from .config import model_config as config
import json

from .prompter import ServicePromptGenerator
from .caller import GptCaller
from ..utils import log_method_call

"""
    This function is responsible for setting up the model to be used in the GPT API
"""
@log_method_call
def setupModel(model_choice: int) -> GptCaller:
        model: str = config["MODEL_CHOICES"][model_choice]
        temperature: float = config["TEMPERATURE"]
        gpt_caller: GptCaller = GptCaller(model=model, temperature=temperature)
        return gpt_caller
    

"""
    This function is responsible for setting up the files to be used inside the prompt
"""
@log_method_call
def setupFiles(performance_path: str):        
    with open(performance_path, 'r') as file:
        performance: dict = json.load(file)
        
    return performance

@log_method_call
def solve(workflow: dict, catalog: dict, model_choice: int):
    gpt_caller: GptCaller = setupModel(model_choice=model_choice)
    
    n_of_generated_services: int = config["N_OF_SERVICES"]
    use_tags: bool = config["USE_TAGS"]
    
    performance: dict = setupFiles(config["PERFORMANCE_PATH"])
    
    prompt: str = ServicePromptGenerator(
        catalog=catalog,
        workflow=workflow,
        performance=performance,
        use_tags=use_tags,
        n=n_of_generated_services
    ).get_prompt()
    
    # Call the GPT API
    response = gpt_caller.call(developer_text=config["DEVELOPER_TEXT"], user_text=prompt)
    
    # Get the result from the response
    result = response.choices[0].message.content
    
    return result