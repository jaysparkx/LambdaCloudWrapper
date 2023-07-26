import json

import pytest
from requests.models import Response
from unittest.mock import patch
from lambda_cloud.instances import LambdaCloudInstance


# Mock the request function
@pytest.fixture(autouse=True)
def mock_request():
    with patch("lambda_cloud.instances.request") as mock:
        yield mock


# Test the LambdaCloudInstance class
class TestLambdaCloudInstance:
    def test_launch_instances(self, mock_request):
        instance = {
            "region_name": "us-tx-1",
            "instance_type_name": "gpu_1x_a100",
            "ssh_key_names": ["macbook-pro"],
            "file_system_names": ["shared-fs"],
            "quantity": 1,
            "name": "training-node-1",
        }
        instance_response = {"data": {"instance_ids": ["0920582c7ff041399e34823a0be62549"]}}
        # Mock the response
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(instance_response).encode("utf-8")
        mock_request.return_value = mock_response

        lambda_cloud_instance = LambdaCloudInstance("api_key")
        result = lambda_cloud_instance.launch_instance(**instance)

        mock_request.assert_called_with(
            "POST",
            "https://cloud.lambdalabs.com/api/v1/instance-operations/launch",
            headers={"Authorization": "Bearer api_key"},
            json=instance,
        )

        assert result == instance_response

    def test_instance_types(self, mock_request):
        instance_types_response = {
            "data": {
                "gpu_1x_a100": {
                    "instance_type": {
                        "name": "gpu_1x_a100",
                        "description": "1x RTX A100 (24 GB)",
                        "price_cents_per_hour": "80",
                        "specs": {"vcpus": 24, "memory_gib": 800, "storage_gib": 512},
                    },
                    "regions_with_capacity_available": [{"name": "us-tx-1", "description": "Austin, Texas"}],
                },
                "gpu_4x_a6000": {
                    "instance_type": {
                        "name": "gpu_4x_a6000",
                        "description": "4x RTX 6000 (24 GB)",
                        "price_cents_per_hour": "110",
                        "specs": {"vcpus": 24, "memory_gib": 800, "storage_gib": 512},
                    },
                    "regions_with_capacity_available": [{"name": "us-az-1", "description": "Phoenix, Arizona"}],
                },
            }
        }

        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(instance_types_response).encode("utf-8")
        mock_request.return_value = mock_response

        lambda_cloud_instance = LambdaCloudInstance("api_key")
        result = lambda_cloud_instance.get_instance_types()

        mock_request.assert_called_with(
            "GET",
            "https://cloud.lambdalabs.com/api/v1/instance-types",
            headers={"Authorization": "Bearer api_key"},
        )
        assert result == instance_types_response

    def test_get_all_instances(self, mock_request):
        instances_response = {
            "data": [
                {
                    "id": "0920582c7ff041399e34823a0be62549",
                    "name": "training-node-1",
                    "ip": "10.10.10.1",
                    "status": "active",
                    "ssh_key_names": ["macbook-pro"],
                    "file_system_names": ["shared-fs"],
                    "region": {"name": "us-tx-1", "description": "Austin, Texas"},
                    "instance_type": {
                        "name": "gpu_1x_a100",
                        "description": "1x RTX A100 (24 GB)",
                        "price_cents_per_hour": 110,
                        "specs": {"vcpus": 24, "memory_gib": 800, "storage_gib": 512},
                    },
                    "hostname": "10-0-8-196.cloud.lambdalabs.com",
                    "jupyter_token": "53968f128c4a4489b688c2c0a181d083",
                    "jupyter_url": "https://jupyter-3ac4c5c6-9026-47d2-9a33-71efccbcd0ee.lambdaspaces.com/?token=53968f128c4a4489b688c2c0a181d083",
                }
            ]
        }

        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(instances_response).encode("utf-8")
        mock_request.return_value = mock_response

        lambda_cloud_instance = LambdaCloudInstance("api_key")
        result = lambda_cloud_instance.get_all_instances()

        mock_request.assert_called_with(
            "GET",
            "https://cloud.lambdalabs.com/api/v1/instances",
            headers={"Authorization": "Bearer api_key"},
        )
        assert result == instances_response

    def test_get_instance(self, mock_request):
        instance_response = {
            "data": {
                "id": "0920582c7ff041399e34823a0be62549",
                "name": "training-node-1",
                "ip": "10.10.10.1",
                "status": "active",
                "ssh_key_names": ["macbook-pro"],
                "file_system_names": ["shared-fs"],
                "region": {"name": "us-tx-1", "description": "Austin, Texas"},
                "instance_type": {
                    "name": "gpu_1x_a100",
                    "description": "1x RTX A100 (24 GB)",
                    "price_cents_per_hour": 110,
                    "specs": {"vcpus": 24, "memory_gib": 800, "storage_gib": 512},
                },
                "hostname": "10-0-8-196.cloud.lambdalabs.com",
                "jupyter_token": "53968f128c4a4489b688c2c0a181d083",
                "jupyter_url": "https://jupyter-3ac4c5c6-9026-47d2-9a33-71efccbcd0ee.lambdaspaces.com/?token=53968f128c4a4489b688c2c0a181d083",
            }
        }

        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(instance_response).encode("utf-8")
        mock_request.return_value = mock_response

        lambda_cloud_instance = LambdaCloudInstance("api_key")
        result = lambda_cloud_instance.get_instance("0920582c7ff041399e34823a0be62549")

        mock_request.assert_called_with(
            "GET",
            "https://cloud.lambdalabs.com/api/v1/instances/0920582c7ff041399e34823a0be62549",
            headers={"Authorization": "Bearer api_key"},
        )
        assert result == instance_response

    def test_terminate_instances(self, mock_request):
        instance_req = ["0920582c7ff041399e34823a0be62549"]
        instance_response = {
            "data": {
                "terminated_instances": [
                    {
                        "id": "0920582c7ff041399e34823a0be62549",
                        "name": "training-node-1",
                        "ip": "10.10.10.1",
                        "status": "active",
                        "ssh_key_names": ["macbook-pro"],
                        "file_system_names": ["shared-fs"],
                        "region": {"name": "us-tx-1", "description": "Austin, Texas"},
                        "instance_type": {
                            "name": "gpu_1x_a100",
                            "description": "1x RTX A100 (24 GB)",
                            "price_cents_per_hour": 110,
                            "specs": {"vcpus": 24, "memory_gib": 800, "storage_gib": 512},
                        },
                        "hostname": "10-0-8-196.cloud.lambdalabs.com",
                        "jupyter_token": "53968f128c4a4489b688c2c0a181d083",
                        "jupyter_url": "https://jupyter-3ac4c5c6-9026-47d2-9a33-71efccbcd0ee.lambdaspaces.com/?token=53968f128c4a4489b688c2c0a181d083",
                    }
                ]
            }
        }

        mock_response = Response()
        mock_response.status_code = 200

        mock_response._content = json.dumps(instance_response).encode("utf-8")
        mock_request.return_value = mock_response

        lambda_cloud_instance = LambdaCloudInstance("api_key")
        result = lambda_cloud_instance.terminate_instance(instance_req)

        mock_request.assert_called_with(
            "POST",
            "https://cloud.lambdalabs.com/api/v1/instance-operations/terminate",
            headers={"Authorization": "Bearer api_key"},
            json={"instance_ids": instance_req},
        )
        assert result == instance_response

    def test_restart_instance(self, mock_request):
        instance_req = ["0920582c7ff041399e34823a0be62549"]
        instance_response = {
            "data": {
                "restarted_instances": [
                    {
                        "id": "0920582c7ff041399e34823a0be62549",
                        "name": "training-node-1",
                        "ip": "10.10.10.1",
                        "status": "active",
                        "ssh_key_names": ["macbook-pro"],
                        "file_system_names": ["shared-fs"],
                        "region": {"name": "us-tx-1", "description": "Austin, Texas"},
                        "instance_type": {
                            "name": "gpu_1x_a100",
                            "description": "1x RTX A100 (24 GB)",
                            "price_cents_per_hour": 110,
                            "specs": {"vcpus": 24, "memory_gib": 800, "storage_gib": 512},
                        },
                        "hostname": "10-0-8-196.cloud.lambdalabs.com",
                        "jupyter_token": "53968f128c4a4489b688c2c0a181d083",
                        "jupyter_url": "https://jupyter-3ac4c5c6-9026-47d2-9a33-71efccbcd0ee.lambdaspaces.com/?token=53968f128c4a4489b688c2c0a181d083",
                    }
                ]
            }
        }

        mock_response = Response()
        mock_response.status_code = 200

        mock_response._content = json.dumps(instance_response).encode("utf-8")
        mock_request.return_value = mock_response

        lambda_cloud_instance = LambdaCloudInstance("api_key")
        result = lambda_cloud_instance.restart_instance(instance_req)

        mock_request.assert_called_with(
            "POST",
            "https://cloud.lambdalabs.com/api/v1/instance-operations/restart",
            headers={"Authorization": "Bearer api_key"},
            json={"instance_ids": instance_req},
        )
        assert result == instance_response
