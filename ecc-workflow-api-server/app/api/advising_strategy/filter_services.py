import json


def filter_services_by_layer(services: dict):
    """
    Filters cloud services for each abstract service based on whether the 
    abstract service's layer is contained in the cloud service's layers.
    
    Args:
        services: Dictionary containing abstract services with their associated cloud services
        
    Returns:
        Dictionary with the same structure as input, but with filtered aws_services arrays
    """
    
    # Create a copy of the original services dictionary to preserve structure
    filtered_services = services.copy()
    filtered_result = []

    for abstract_service in services.get('result', []):
        # Get the abstract service layer
        abstract_layer = abstract_service.get('abstractservice_layer')
        
        if not abstract_layer:
            # If no layer specified, keep the service as is
            filtered_result.append(abstract_service)
            continue
        
        # Filter cloud services
        filtered_cloud_services = []
        for cloud_service in abstract_service.get('aws_services', []):
            service_layers = cloud_service.get('service_layers', [])
            
            # Check if abstract service layer is in cloud service layers
            if abstract_layer in service_layers:
                filtered_cloud_services.append(cloud_service)
        
        # Create a copy of the abstract service with filtered cloud services
        filtered_abstract_service = abstract_service.copy()
        filtered_abstract_service['aws_services'] = filtered_cloud_services
        
        filtered_result.append(filtered_abstract_service)
    
    # Update the result array in the copied dictionary
    filtered_services['result'] = filtered_result
    
    return filtered_services
