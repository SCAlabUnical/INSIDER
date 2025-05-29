import json
from abc import ABC, abstractmethod
from ..utils import log_method_call

class PromptGenerator(ABC):
    @abstractmethod
    def get_prompt(self):
        pass
    
    
class ServicePromptGenerator(PromptGenerator):
    @log_method_call
    def __init__(self, catalog: dict, workflow: dict, performance: dict, use_tags=False, n: int = 3):        
        
        # The following text will be added only if use_tags is True
        tags_workflow_description = (
            "The tags field is a list of tags that can be used to find the best concrete service from the catalog. "
            "Particularly, this tags are used to find additional services that don't match the other criterias. "
            if use_tags else ""
        )
        workflow_description: str = (
            "Each element of the workflow is an abstract service that I want to associate to a concrete AWS service. "
            "Here is the workflow: \n\n"
            f"{json.dumps(workflow, indent=4)}\n\n"
            "The workflow is a json containing a list of elements, each element having the following fields: "
            "The name field is the name of the abstract service that I want to associate to a concrete AWS service. "
            "The id field is the id of the abstract service. "
            "The type of the abstract service is given by the type field. To this abstract service can only be associated a "
            "concrete service of the same type. "
            "The description field contains a short description of the abstract service and it should "
            "be used together with the type field in order to find the best concrete service from the catalog."
            "The parameters are a set of parameters that the abstract service imposes when finding a solution. "
            f"{tags_workflow_description}"
        )
        
        layer_description: str = (
            'Starting from the workflow that I have given you, to each abstractservice I want you to add a field called '
            'abstractservice_layer. This field dependes on the parameters of each service. Particularly, starting from this json file: '
            f'{json.dumps(performance, indent=4)}\n\n'
            'I want you to select a layer for each abstract service. The layer is selected matching the parameters of the abstract service '
            'with the parameters of a layer from the performance json. The layer is a string that represents the layer of the abstract service '
            'and needs to be added to each abstractservice in the workflow as a field with name abstractservice_layer. '
        )
        
        tags_catalog_description = (
            "The service tags is a list of tags that can be used to find the best service for an abstract service. "
            if use_tags else ""
        )
        catalog_description: str = (
            "I also have a catalog of services that I want to use: \n\n"
            f"{json.dumps(catalog, indent=4)}\n\n"
            "Each element of the catalog is a concrete AWS service that can be associated to an abstract service. "
            "Each service has 11 fields. The Service Name is the name of the service, the ID is the id of the service, "
            "The Service Type is the type of the service and it MUST be the same as the type of the abstract service. "
            f"{tags_catalog_description}"
            f"To each element of the workflow I want to associate up to {n} concrete AWS services from the catalog. "
            "It is important that you take only services from the catalog and that the services are of the same type as the abstract service."
        )
        
        tags_response_description_1 = (
            ", the tags of the abstract service called abstractservice_tags"
            if use_tags else ""
        )
        
        tags_response_description_2 = (
            ", the tags of the service called service_tags, that can be used to add additional services that don't follow the other criterias "
            if use_tags else ""
        )
        response_description: str = (
            " As a result I want you to give me a json file but in plain text format, without any formatting whatsoever. "
            "The json contains an element called result that contains a list of elements, and "
            "each element has the following fields: the id of the abstract service called abstractservice_id, "
            "the name of the abstract service, called abstractservice_name, the type of the abstract service called abstractservice_type, "
            "the description of the abstract service, called abstractservice_description, "
            "the layer of the abstract service called abstractservice_layer, calculated previously matching the parameters of the service "
            f"{tags_response_description_1}"
            " and the list of suggested AWS services called aws_services selected from the catalog. For each of the suggested services, I want you to "
            "insert in the json the following fields: the id of the service called service_id, the name of the service called service_name, the layers array "
            "where the concrete service can be deployed, called service_layers "
            f"{tags_response_description_2}"
            " and the type of the service called service_type. "
            "Please ensure that the output does not include any ```json or other code block delimiters."
            "Given the catalog and the workflow, I want you to suggest the best AWS service from the catalog for each element of the workflow. "
            f"You can suggest up to {n} services for each element. "
        )
        
        self.prompt: str = workflow_description + layer_description + catalog_description + response_description

    @log_method_call
    def get_prompt(self):
        return self.prompt
