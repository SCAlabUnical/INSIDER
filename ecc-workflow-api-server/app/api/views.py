from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
import logging

from .advising_strategy.AdvisingStrategy import AdvisingStrategy, GPTAdvisingStrategy
from .solving_strategy.LLMStrategy import LLMStrategy
from .solving_strategy.LinearStrategy import LinearStrategy
from django.urls import path

@api_view(['GET', 'POST'])
def home(request):
    logging.info("API Called: home")
    response = JsonResponse(
        {
            'message': 'Welcome to the Workflow Service Optimizer API'
        }, 
        status=200
    )
    
    logging.info("API Finished: sent response to client")
    logging.debug(f"Response: {response}")
    
    return response

@api_view(['GET', 'POST'])
def solve_with_llm(request, model_id):
    logging.info(f"API Called: solve_with_llm with model_id: {model_id}")
    
    request_body = json.loads(request.body)
    
    workflow: dict = request_body[0]
    catalog: dict = request_body[1]
    
    strategy = LLMStrategy()
    
    response = JsonResponse(
        {
            'message': 'Solving with LLM',
            'request_body': strategy.solve(workflow, catalog, model_id)
        }, 
        status=200
    )
    
    return response

@api_view(['GET', 'POST'])
def solve_with_linear(request):
    logging.info(f"API Called: solve_with_linear")
    
    request_body = json.loads(request.body)
    print("[DEBUG] Raw request body:", request.body)
    print("[DEBUG] Parsed request_body:", request_body)
    print("[DEBUG] Type of workflow:", type(request_body[0]))
    print("[DEBUG] Type of catalog:", type(request_body[1]))

    workflow: dict = request_body[0]
    catalog = request_body[1]
    
    # If catalog is a string, parse it
    if isinstance(catalog, str):
        print("[DEBUG] Catalog is a string, parsing JSON...")
        catalog = json.loads(catalog)
    else:
        print("[DEBUG] Catalog is already a dict.")
    
    strategy = LinearStrategy()
    
    response = JsonResponse(
        {
            'message': 'Solving with Linear',
            'request_body': strategy.solve(workflow, catalog)
        }, 
        status=200
    )
    
    return response

@api_view(['GET', 'POST'])
def advise_solution(request, model_id):
    logging.info(f"API Called: advise_solution")
    
    try:
        request_body = json.loads(request.body)
        services = request_body
        # If services is a list, wrap it in a dict with key 'result' to match advisor.py expectations
        if isinstance(services, list):
            services = {"result": services}
        logging.debug(f"[DEBUG] Services received for advising: {services}")
        logging.debug(f"[DEBUG] Type of services: {type(services)}")
        logging.debug(f"[DEBUG] model_id: {model_id}, type: {type(model_id)}")
        strategy: AdvisingStrategy = GPTAdvisingStrategy()
        logging.debug("[DEBUG] Calling strategy.advise_solution...")
        result = strategy.advise_solution(services, model_id)
        logging.debug(f"[DEBUG] Result from advise_solution: {result}")
        response = JsonResponse(
            {
                'message': 'Advising solution',
                'request_body': result
            }, 
            status=200
        )
    except Exception as e:
        logging.error(f"Error in advise_solution: {str(e)}")
        import traceback
        traceback.print_exc()  # Print the full traceback to the logs
        response = JsonResponse(
            {
                'error': 'Failed to process request',
                'details': str(e)
            },
            status=500
        )
    
    return response

