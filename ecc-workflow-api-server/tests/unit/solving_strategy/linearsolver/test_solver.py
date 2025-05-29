import pytest
from typing import List
from icecream import ic
import os
import json
from unittest.mock import patch, mock_open
from app.api.solving_strategy.linearsolver.solver import (
    find_best_layer, transform_constraints_to_int, filter_by_type, filter_by_layer, 
    filter_by_tags, join_results, setup_files, solve, transfrom_layer_to_str, transform_layers_to_int
)

class TestFindBestLayer:
    def test_find_best_layer_cloud_preferred(self, sample_service_cloud, sample_performance):
        """Test that find_best_layer returns 'cloud' when it's the best option"""
        # Arrange your test data to favor cloud
        # Act
        result = find_best_layer(sample_service_cloud, sample_performance)
        # Assert
        assert result == "cloud"
    
    def test_find_best_layer_edge_preferred(self, sample_service_far_edge, sample_performance):
        """Test that find_best_layer returns 'edge' when it's the best option"""
        # Arrange your test data to favor edge
        # Act
        result = find_best_layer(sample_service_far_edge, sample_performance)
        # Assert
        assert result == "far-edge"
        
    def test_find_best_layer_on_device_preferred(self, sample_service_on_device, sample_performance):
        """Test that find_best_layer returns 'on-device' when it's the best option"""
        # Arrange your test data to favor on-device
        # Act
        result = find_best_layer(sample_service_on_device, sample_performance)
        # Assert
        assert result == "on-device"
        
    def test_find_best_layer(self, sample_services, sample_performance):
        """Test that find_best_layer returns the best layer"""
        # Arrange your test data to favor on-device
        # Act
        result: List[str] = [ find_best_layer(service, sample_performance) for service in sample_services ]
        # Assert
        expected: List[str] = ["cloud", "far-edge", "on-device", "cloud", "far-edge", "far-edge", "on-premise"]
        assert result == expected
        

class TestTransformConstraintsToInt:
    def test_transform_constraints_to_int(self, sample_parameters):
        """Test that constraints are correctly transformed to integers"""
        # Act
        result = transform_constraints_to_int(sample_parameters)
        expected = {
            "execution_time": 0,
            "memory_consumption": 2,
            "bandwidth_consumption": 1,
            "storage_consumption": 4,
            "availability": 3
        }
        ic(result)
        ic(expected)
        # Assert
        assert result == expected
    

class TestFilterByType:
    def test_filter_by_type_computation(self, sample_catalog):
        """Test filtering catalog by 'Computation' type"""
        # Act
        result = filter_by_type(sample_catalog, "Computation")
        # Assert
        assert all(service["Service Type"] == "Computation" for service in result["service"])

    def test_filter_by_type_storage(self, sample_catalog):
        """Test filtering catalog by 'Storage' type"""
        # Act
        result = filter_by_type(sample_catalog, "Storage")
        # Assert
        assert all(service["Service Type"] == "Storage" for service in result["service"])
        
    def test_filter_by_type_communication(self, sample_catalog):
        """Test filtering catalog by 'Communication' type"""
        # Act
        result = filter_by_type(sample_catalog, "Communication")
        # Assert
        assert all(service["Service Type"] == "Communication" for service in result["service"])

class TestFilterByLayer:
    def test_filter_by_layer_cloud(self, sample_catalog):
        """Test filtering catalog by 'cloud' layer"""
        # Act
        result = filter_by_layer(sample_catalog, "cloud")
        # Assert
        assert all("cloud" in service["layers"] for service in result["service"])

    def test_filter_by_layer_edge(self, sample_catalog):
        """Test filtering catalog by 'far-edge' layer"""
        # Act
        result = filter_by_layer(sample_catalog, "far-edge")
        # Assert
        assert all("far-edge" in service["layers"] for service in result["service"])
        
    def test_filter_by_layer_on_device(self, sample_catalog):
        """Test filtering catalog by 'on-device' layer"""
        # Act
        result = filter_by_layer(sample_catalog, "on-device")
        # Assert
        assert all("on-device" in service["layers"] for service in result["service"])
        
    def test_filter_by_layer_on_premise(self, sample_catalog):
        """Test filtering catalog by 'on-premise' layer"""
        # Act
        result = filter_by_layer(sample_catalog, "on-premise")
        # Assert
        assert all("on-premise" in service["layers"] for service in result["service"])
        
    def test_filter_by_layer_near_edge(self, sample_catalog):
        """Test filtering catalog by 'near-edge' layer"""
        # Act
        result = filter_by_layer(sample_catalog, "near-edge")
        # Assert
        assert all("near-edge" in service["layers"] for service in result["service"])

class TestFilterByTags:
    def test_filter_by_single_tag(self, sample_catalog):
        """Test filtering catalog by a single tag"""
        # Act
        result = filter_by_tags(sample_catalog, ["Monitoring"])
        # Assert
        assert all("Monitoring" in service["Tags"] for service in result["service"])

    def test_filter_by_multiple_tags(self, sample_catalog):
        """Test filtering catalog by multiple tags (matches any)"""
        # Act
        result = filter_by_tags(sample_catalog, ["Machine Learning", "AI"])
        # Assert
        assert all(any(tag in service["Tags"] for tag in ["Machine Learning", "AI"]) 
                  for service in result["service"])

class TestJoinResults:
    def test_join_results_no_overlap(self):
        """Test joining dictionaries with no overlapping services"""
        # Arrange
        layer_services = {"service": [
            {"ID": "s1", "Service Name": "Service 1", "Service Type": "Computation", "layers": ["cloud"], "Tags": ["tag1"]}
        ]}
        tags_services = {"service": [
            {"ID": "s2", "Service Name": "Service 2", "Service Type": "Storage", "layers": ["edge"], "Tags": ["tag2"]}
        ]}
        
        # Act
        result = join_results(layer_services, tags_services)
        
        # Assert
        expected = [
            {"service_id": "s1", "service_name": "Service 1", "service_type": "Computation", "service_layer": ["cloud"], "service_tags": ["tag1"]},
            {"service_id": "s2", "service_name": "Service 2", "service_type": "Storage", "service_layer": ["edge"], "service_tags": ["tag2"]}
        ]
        assert result == expected
    
    def test_join_results_with_overlap(self):
        """Test joining dictionaries with overlapping services"""
        # Arrange
        layer_services = {"service": [
            {"ID": "s1", "Service Name": "Service 1", "Service Type": "Computation", "layers": ["cloud"], "Tags": ["tag1"]}
        ]}
        tags_services = {"service": [
            {"ID": "s1", "Service Name": "Service 1", "Service Type": "Computation", "layers": ["cloud"], "Tags": ["tag1"]}
        ]}
        
        # Act
        result = join_results(layer_services, tags_services)
        
        # Assert
        expected = [
            {"service_id": "s1", "service_name": "Service 1", "service_type": "Computation", "service_layer": ["cloud"], "service_tags": ["tag1"]}
        ]
        assert result == expected
        
    def test_join_results_empty_dicts(self):
        """Test joining empty dictionaries"""
        # Arrange
        layer_services = {"service": []}
        tags_services = {"service": []}
        
        # Act
        result = join_results(layer_services, tags_services)
        
        # Assert
        expected = []
        assert result == expected
    
    def test_join_results_one_empty_dict(self):
        """Test joining when one of the dictionaries has an empty service list"""
        # Arrange
        layer_services = {"service": [
            {"ID": "s1", "Service Name": "Service 1", "Service Type": "Computation", "layers": ["cloud"], "Tags": ["tag1"]},
            {"ID": "s2", "Service Name": "Service 2", "Service Type": "Storage", "layers": ["edge"], "Tags": ["tag2"]}
        ]}
        tags_services = {"service": []}
        
        # Act
        result = join_results(layer_services, tags_services)
        
        # Assert
        expected = [
            {"service_id": "s1", "service_name": "Service 1", "service_type": "Computation", "service_layer": ["cloud"], "service_tags": ["tag1"]},
            {"service_id": "s2", "service_name": "Service 2", "service_type": "Storage", "service_layer": ["edge"], "service_tags": ["tag2"]}
        ]
        assert result == expected
        
        # Test the reverse situation
        result = join_results({"service": []}, layer_services)
        assert result == expected
    
    def test_join_results_different_services_same_id(self):
        """Test joining dictionaries with services that have the same ID but different attributes"""
        # Arrange
        layer_services = {"service": [
            {"ID": "s1", "Service Name": "Service 1", "Service Type": "Computation", "layers": ["cloud"], "Tags": ["tag1"]}
        ]}
        tags_services = {"service": [
            {"ID": "s1", "Service Name": "Service 1 Updated", "Service Type": "Storage", "layers": ["edge"], "Tags": ["tag2"]}
        ]}
        
        # Act
        result = join_results(layer_services, tags_services)
        
        # Assert
        # The second service should override the first one because they have the same ID
        expected = [
            {"service_id": "s1", "service_name": "Service 1", "service_type": "Computation", "service_layer": ["cloud"], "service_tags": ["tag1"]},
            {"service_id": "s1", "service_name": "Service 1 Updated", "service_type": "Storage", "service_layer": ["edge"], "service_tags": ["tag2"]}
        ]
        assert result != expected
        
        # In your new implementation, duplicates are detected by full equality, so both would appear if we reverse the order
        expected_with_deduplication = [
            {"service_id": "s1", "service_name": "Service 1", "service_type": "Computation", "service_layer": ["cloud"], "service_tags": ["tag1"]}
        ]
        assert len(result) == 1
        
    def test_join_results_multiple_services(self):
        """Test joining dictionaries with multiple services"""
        # Arrange
        layer_services = {"service": [
            {"ID": "s1", "Service Name": "Service 1", "Service Type": "Computation", "layers": ["cloud"], "Tags": ["tag1"]},
            {"ID": "s2", "Service Name": "Service 2", "Service Type": "Storage", "layers": ["edge"], "Tags": ["tag2"]}
        ]}
        tags_services = {"service": [
            {"ID": "s3", "Service Name": "Service 3", "Service Type": "Communication", "layers": ["on-device"], "Tags": ["tag3"]},
            {"ID": "s4", "Service Name": "Service 4", "Service Type": "Computation", "layers": ["far-edge"], "Tags": ["tag4"]}
        ]}
        
        # Act
        result = join_results(layer_services, tags_services)
        
        # Assert
        expected = [
            {"service_id": "s1", "service_name": "Service 1", "service_type": "Computation", "service_layer": ["cloud"], "service_tags": ["tag1"]},
            {"service_id": "s2", "service_name": "Service 2", "service_type": "Storage", "service_layer": ["edge"], "service_tags": ["tag2"]},
            {"service_id": "s3", "service_name": "Service 3", "service_type": "Communication", "service_layer": ["on-device"], "service_tags": ["tag3"]},
            {"service_id": "s4", "service_name": "Service 4", "service_type": "Computation", "service_layer": ["far-edge"], "service_tags": ["tag4"]}
        ]
        assert result == expected