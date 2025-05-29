import json
import pytest
import os

@pytest.fixture
def sample_workflow():
    """Load sample workflow data"""
    file_path = os.path.join(os.path.dirname(__file__), '../../../fixtures/sample_workflow.json')
    with open(file_path, 'r') as file:
        return json.load(file)
    
@pytest.fixture
def sample_service_on_device():
    """Load sample service data for on-device execution"""
    file_path = os.path.join(os.path.dirname(__file__), '../../../fixtures/sample_service_on_device.json')
    with open(file_path, 'r') as file:
        return json.load(file)
    
@pytest.fixture
def sample_service_far_edge():
    """Load sample service data for far-edge execution"""
    file_path = os.path.join(os.path.dirname(__file__), '../../../fixtures/sample_service_far_edge.json')
    with open(file_path, 'r') as file:
        return json.load(file)
    
@pytest.fixture
def sample_service_cloud():
    """Load sample service data for cloud execution"""
    file_path = os.path.join(os.path.dirname(__file__), '../../../fixtures/sample_service_cloud.json')
    with open(file_path, 'r') as file:
        return json.load(file)
    
@pytest.fixture
def sample_services():
    """Load sample services data"""
    file_path = os.path.join(os.path.dirname(__file__), '../../../fixtures/sample_services.json')
    with open(file_path, 'r') as file:
        return json.load(file)
    
@pytest.fixture
def sample_parameters():
    """Load sample parameters data"""
    file_path = os.path.join(os.path.dirname(__file__), '../../../fixtures/sample_parameters.json')
    with open(file_path, 'r') as file:
        return json.load(file)

@pytest.fixture
def sample_catalog():
    """Load sample catalog data"""
    file_path = os.path.join(os.path.dirname(__file__), '../../../fixtures/sample_catalog.json')
    with open(file_path, 'r') as file:
        return json.load(file)

@pytest.fixture
def sample_performance():
    """Load sample performance data"""
    file_path = os.path.join(os.path.dirname(__file__), '../../../fixtures/sample_performance.json')
    with open(file_path, 'r') as file:
        return json.load(file)
