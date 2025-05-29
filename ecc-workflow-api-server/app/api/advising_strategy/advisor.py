import json
from ..solving_strategy.gptsolver.config import model_config as config
from ..solving_strategy.gptsolver.caller import GptCaller
from ..solving_strategy.utils import log_method_call
from ..solving_strategy.gptsolver.config import model_config as config
from .filter_services import filter_services_by_layer
from icecream import ic

"""
    This function is responsible for setting up the files to be used inside the prompt

"""
@log_method_call
def setupModel(model_choice: int) -> GptCaller:
        model: str = config["MODEL_CHOICES"][model_choice]
        temperature: float = config["TEMPERATURE"]
        gpt_caller: GptCaller = GptCaller(model=model, temperature=temperature)
        return gpt_caller

@log_method_call
def advise_partitioned_services(partitioned_services: dict, model_choice: int) -> dict:
    # Only log partition index and prompt/response lengths, not full data
    gpt_caller: GptCaller = setupModel(model_choice=model_choice)

    prompt: str = (
        "# Multi-Cloud Workflow Service Optimization Task\n\n"
        "## Context\n"
        "You are an expert cloud architect specializing in multi-cloud solutions including AWS, Azure, and Google Cloud Platform (GCP). "
        "Your task is to analyze a set of abstract services in a workflow and recommend the most appropriate cloud service implementation for each from any major cloud provider.\n\n"
        
        "## Input Data\n"
        "I will provide you with a JSON structure containing abstract services and potential cloud service implementations.\n"
        f"{json.dumps(partitioned_services, indent=4)}\n\n"
        
        "## Service Structure\n"
        "Each service in the workflow contains the following information:\n"
        "- abstractservice_id: Unique identifier for the abstract service\n"
        "- abstractservice_name: Name describing the service's function\n"
        "- abstractservice_layer: Deployment layer (cloud, on-premise, edge, etc.)\n"
        "- abstractservice_description: Description of the service's purpose and functionality\n"
        "- abstractservice_tags: Tags describing characteristics and capabilities\n"
        "- aws_services: List of potential services from various cloud providers (AWS, Azure, GCP) that could implement this abstract service\n\n"
        
        "## Task Instructions\n"
        "1. For each abstract service, select the SINGLE BEST cloud service from the available options in the aws_services array ONLY.\n"
        "2. The best_service field must be the service_name of one of the objects in the aws_services array for that service.\n"
        "3. Consider services from any major cloud provider (AWS, Azure, GCP) based on compatibility, suitability, and best practices.\n\n"
        
        "## Response Format\n"
        "Create a NEW JSON structure with ONLY the following fields for each service (copy from input unless otherwise specified):\n"
        "- abstractservice_id\n"
        "- abstractservice_name\n"
        "- abstractservice_layer\n"
        "- best_service: The service_name of the single best cloud service you recommend, chosen ONLY from the aws_services array above.\n"
        "\n"
        "## Response Example\n"
        "```json\n"
        "{\n"
        "  \"result\": [\n"
        "    { \"abstractservice_id\": 0, \"abstractservice_name\": \"Web Interface\", \"abstractservice_layer\": \"far-edge\", \"best_service\": \"Amazon API Gateway\" },\n"
        "    { \"abstractservice_id\": 1, \"abstractservice_name\": \"Publish-Subscribe Broker\", \"abstractservice_layer\": \"far-edge\", \"best_service\": \"Amazon Simple Notification Service\" }\n"
        "  ]\n"
        "}\n"
        "```\n"
        "\n"
        "## Response Requirements\n"
        "- Return ONLY plain text JSON with no additional commentary or markdown\n"
        "- For each service, include ONLY the fields: abstractservice_id, abstractservice_name, abstractservice_layer, best_service\n"
        "- The best_service value MUST be the service_name of one of the objects in the aws_services array for that service.\n"
        "- Ensure the response is valid JSON that can be parsed\n"
        "- Be consistent in your formatting across all services\n"
        "- The JSON must be complete - make sure to include ALL services from the input\n"
    )

    ic("Prompt length", len(prompt))
    response = gpt_caller.call(developer_text=config["DEVELOPER_TEXT"], user_text=prompt)
    raw_result = response.choices[0].message.content if response.choices and len(response.choices) > 0 else ""
    ic("Raw LLM result length", len(raw_result) if raw_result else 0)
    # Only log first 200 chars if error

    cleaned_result = ""
    if raw_result:
        cleaned_result = raw_result.strip()
        if cleaned_result.startswith("```json"):
            cleaned_result = cleaned_result.replace("```json", "", 1)
        if cleaned_result.startswith("```"):
            cleaned_result = cleaned_result.replace("```", "", 1)
        if cleaned_result.endswith("```"):
            cleaned_result = cleaned_result[:-3]

    try:
        parsed_json = json.loads(cleaned_result)
        # Only log type and length of parsed result
        ic("Parsed JSON type", type(parsed_json))
        if isinstance(parsed_json, dict):
            ic("Parsed JSON keys", list(parsed_json.keys()))
        return parsed_json
    except json.JSONDecodeError as e:
        ic("JSON decode error", str(e))
        ic("Raw LLM result (first 200 chars)", raw_result[:200] if raw_result else "")
        return {
            "error": "Invalid JSON response", 
            "details": str(e),
            "raw_content_first_200": raw_result[:200] if raw_result else ""
        }

def advise(services: dict, model_choice: int) -> dict:
    # Only log partition index and error count, not full data
    NUM_SERVICES_PER_PART = 5

    layer_services: dict = filter_services_by_layer(services)

    partitioned_services = divide_services(layer_services, NUM_SERVICES_PER_PART)

    all_results = []
    errors = []
    for idx, part in enumerate(partitioned_services):
        ic(f"Partition {idx} size", len(part.get("result", [])))
        result = advise_partitioned_services(part, model_choice)
        if "result" in result:
            all_results.append(result)
        else:
            errors.append({"partition": idx, "error": result})

    # The expected structure of the result is {"result": [...]}, not a list
    # So we need to combine all the results into a single dict with "result" as the key
    combined_result = {"result": []}
    for res in all_results:
        if "result" in res:
            combined_result["result"].extend(res["result"])

    if errors:
        ic("Partition errors count", len(errors))
        combined_result["errors"] = errors
    ic("Total services advised", len(combined_result["result"]))
    return combined_result

@log_method_call
def divide_services(services: dict, num_services_par_part: int) -> list:
    """
    Divides the services['result'] list into parts of a specified size.
    Returns a list of dicts, each with the same structure as the input (i.e., {"result": [...]})
    """
    all_services = services.get("result", [])
    divided_services = []
    for i in range(0, len(all_services), num_services_par_part):
        part = all_services[i:i + num_services_par_part]
        divided_services.append({"result": part})
    return divided_services