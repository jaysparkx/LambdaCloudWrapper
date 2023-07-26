import json

import pytest
from requests.models import Response
from unittest.mock import patch
from lambda_cloud.file_systems import LambdaCloudFileSystem


# Mock the request function
@pytest.fixture(autouse=True)
def mock_request():
    with patch("lambda_cloud.file_systems.request") as mock:
        yield mock


# Test the LambdaCloudFileSystem class
class TestLambdaCloudFileSystem:
    def test_get_all_instances(self, mock_request):
        instances_response = {
            "data": [
                {
                    "id": "0920582c7ff041399e34823a0be62547",
                    "name": "shared-fs",
                    "created": "2023-02-24T20:48:56+00:00",
                    "created_by": {
                        "id": "0920582c7ff041399e34823a0be62549",
                        "email": "teammate@example.com",
                        "status": "active",
                    },
                    "mount_point": "/home/ubuntu/shared-fs",
                    "region": {"name": "us-tx-1", "description": "Austin, Texas"},
                    "is_in_use": True,
                }
            ]
        }

        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(instances_response).encode("utf-8")
        mock_request.return_value = mock_response

        lambda_cloud_file_system = LambdaCloudFileSystem("api_key")
        result = lambda_cloud_file_system.get_file_systems()

        mock_request.assert_called_with(
            "GET",
            "https://cloud.lambdalabs.com/api/v1/file-systems",
            headers={"Authorization": "Bearer api_key"},
        )
        assert result == instances_response
