import os
import json
from typing import List, Dict
from .config import solver_config as config
from ..utils import log_method_call

# Logging configuration
import logging
log_path = './app/api/logs/linearsolver-solver.log'
os.makedirs(os.path.dirname(log_path), exist_ok=True)
if not os.path.exists(log_path):
    with open(log_path, 'w', encoding='utf-8') as f:
        pass
LOGGING_LEVEL = logging.DEBUG
logging.basicConfig(filename=log_path, format='%(asctime)s - %(levelname)s:%(message)s', filemode='w', encoding='utf-8', level=LOGGING_LEVEL, datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

@log_method_call
def solve(workflow: dict, catalog: str) -> dict:
    """
    Solve the workflow using the catalog.
    
    Args:
        workflow: Dictionary containing the workflow
        catalog_str: JSON string containing the catalog
        
    Returns:
        Dictionary with the solution
    """
    logging.debug("[solve] Solving workflow with args: %s\n", workflow)
    logging.debug("[solve] Solving workflow with catalog: %s", catalog)

    # Convert Tags field from string to list of strings for each service
    for service in catalog.get("service", []):
        tags = service.get("Tags")
        if isinstance(tags, str):
            service["Tags"] = [tag.strip() for tag in tags.split(",") if tag.strip()]

    performance: dict = setup_files(config["PERFORMANCE_PATH"])
    
    final_result: dict = {
        "result": []
    }
    
    for node in workflow["nodes"]:
        logging.debug("[solve] Solving node: %s", node)
        # Find the layer on which the node will be executed
        layer: str = find_best_layer(node, performance)
        
        # Filter the catalog including only the services that of the same type as the selected service
        type_services: dict = filter_by_type(catalog, node["type"])
    
        # Filter the catalog including only the services that can be executed on the selected layer
        layer_services: dict = filter_by_layer(type_services, layer)
        
        # Filter the catalog including only the services with at least one of the selected tags
        if "tags" in node:
            logging.debug("[solve] Filtering by tags: %s", node["tags"])
            tags_services: dict = filter_by_tags(type_services, node["tags"])
        else:
            logging.warning("[solve] No tags found for node: %s", node)
            tags_services: dict = {'service': []}
        
        # Join layer_services and tag_services in a single dictionary
        matching_services: dict = join_results(layer_services, tags_services)
        
        # Setup the result dictionary
        final_result["result"].append({
            "abstractservice_id": node["id"],
            "abstractservice_name": node["name"],
            "abstractservice_type": node["type"],
            "abstractservice_description": node["description"] if "description" in node else "",
            "abstractservice_layer": layer,
            "abstractservice_tags": node["tags"] if "tags" in node else [],
            "aws_services": matching_services
        })
    
    return final_result

@log_method_call
def setup_files(performance_path: str) -> dict:
    """
    This function is responsible for setting up the files to be used inside the prompt
    """    
    try:
        with open(performance_path, 'r') as file:
            performance: dict = json.load(file)
        return performance
    except Exception as e:
        raise

@log_method_call
def find_best_layer(service: dict, performance: dict) -> str:
    """
    Based on the performance json file, this function returns the best layer for the service to be executed.
    The performance file is a dictionary where the keys are constraints that the service must satisfy to be executed on that layer.
    Each value can assume one of the following: very low, low, moderate, high, very high.
    The layers are: cloud, far-edge, near-edge, on-premise and on-device.
    """
    parameters: dict = service["parameters"]
    
    # Transform the constraints from string to integer
    transformed_parameters: Dict[str, int] = transform_constraints_to_int(parameters)
    
    # Transform the constraints from string to integer
    transformed_performance: Dict[str, Dict[str, int]] = {}
    for layer, constraints in performance.items():
        transformed_performance[layer] = transform_constraints_to_int(constraints)
        
    # Transform the layers from string to integer in order to take the minimum layer using the pre-defined order
    transformed_performance: Dict[int, Dict[str, int]] = transform_layers_to_int(transformed_performance)
    
    '''
        Using an array of countings, we will count the number of constraints satisfied for each layer.
        The i index of the array will rappresent the number of constraints satisfied for the layer i.
        The mapping for the layers is the following:
        cloud -> 4
        far-edge -> 3
        near-edge -> 2
        on-premise -> 1
        on-device -> 0
    '''
    constraints_satisfied: List[int] = [0, 0, 0, 0, 0]
    for service_constraint, value in transformed_parameters.items():
        for layer, constraints in transformed_performance.items():
            if constraints[service_constraint] >= value:
                constraints_satisfied[layer] += 1
    
    # The best layer is the layer that satisfies the most constraints but with the lowest index
    best_layer: int = constraints_satisfied.index(max(constraints_satisfied))
    
    best_layer_str: str = transfrom_layer_to_str(best_layer)
    
    # Return the layer with the highest number of constraints satisfied    
    return best_layer_str

@log_method_call
def transform_constraints_to_int(parameters: Dict[str, str]) -> Dict[str, int]:
    """
    Transforms the constraints from string to integer.
    The mapping is the following:
    very low -> 0
    low -> 1
    moderate -> 2
    high -> 3
    very high -> 4
    """
    mappings: Dict[str, int] = {
        "very low": 0,
        "low": 1,
        "moderate": 2,
        "high": 3,
        "very high": 4
    }
    
    result = {}
    for key, value in parameters.items():
        result[key] = mappings[value]
        
    return result

@log_method_call
def transform_layers_to_int(performance: Dict[str, Dict[str, int]]) -> Dict[int, Dict[str, int]]:
    """
    Transforms the layers from string to integer.
    The mapping is the following:
    cloud -> 4
    near-edge -> 3
    far-edge -> 2
    on-premise -> 1
    on-device -> 0
    """
    mappings: Dict[str, int] = {
        "cloud": 4,
        "near-edge": 3,
        "far-edge": 2,
        "on-premise": 1,
        "on-device": 0
    }
    
    result = {}
    for key, value in performance.items():
        result[mappings[key]] = value
        
    return result

@log_method_call
def transfrom_layer_to_str(layer: int) -> str:
    """
    Transforms the layers from integer to string.
    The mapping is the following:
    4 -> cloud
    3 -> near-edge
    2 -> far-edge
    1 -> on-premise
    0 -> on-device
    """
    mappings: Dict[int, str] = {
        4: "cloud",
        3: "near-edge",
        2: "far-edge",
        1: "on-premise",
        0: "on-device"
    }
    
    return mappings[layer]

@log_method_call
def filter_by_type(catalog: dict, service_type: str) -> dict:
    """
    Filters the catalog by service type.
    """
    logging.debug("[filter_by_type] Filtering catalog by service type: %s", service_type)
    result: dict = catalog.copy()
    result["service"] = [service for service in catalog["service"] if service["Service Type"] == service_type]
    return result

@log_method_call
def filter_by_layer(catalog: dict, layer: str) -> dict:
    """
    Filters the catalog by layer.
    """
    result: dict = catalog.copy()
    result["service"] = [service for service in catalog["service"] if layer in service["layers"]]
    return result

@log_method_call
def filter_by_tags(catalog: dict, tags: list) -> dict:
    """
    Filters the catalog by tags.
    """
    result: dict = catalog.copy()
    logging.debug("[filter_by_tags] Filtering catalog by tags: %s", tags)
    result["service"] = [service for service in catalog["service"] if any(tag in service["Tags"] for tag in tags)]
    return result

@log_method_call
def join_results(dict1: dict, dict2: dict) -> dict:
    """
    Combines two dictionaries into a single dictionary.
    Handles merging of nested dictionaries and lists.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        A merged dictionary combining contents from both input dictionaries in the determined format
    """
    result: list = []

    logging.debug("[join_results] Joining results from two dictionaries")
    logging.debug("[join_results] Dictionary 1: %s", dict1)
    logging.debug("[join_results] Dictionary 2: %s", dict2)
    
    # Add the services from the first dictionary following the desired format
    for service in dict1["service"]:
        formatted_service = {
            "service_id": service["ID"],
            "service_name": service["Service Name"],
            "service_type": service["Service Type"],
            "service_layers": service["layers"],
            "service_tags": service["Tags"]
        }
        
        result.append(formatted_service)
        
    # Add the services from the second dictionary following the desired format
    for service in dict2["service"]:
        formatted_service = {
            "service_id": service["ID"],
            "service_name": service["Service Name"],
            "service_type": service["Service Type"],
            "service_layers": service["layers"],
            "service_tags": service["Tags"]
        }
        
        # If there is no service with the same ID in the result list, add the service
        if formatted_service["service_id"] not in [service["service_id"] for service in result]:
            result.append(formatted_service)
            
    return result

