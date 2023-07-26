import json

import pytest
from requests.models import Response
from unittest.mock import patch
from lambda_cloud.ssh_keys import LambdaCloudSshKey


# Mock the request function
@pytest.fixture(autouse=True)
def mock_request():
    with patch("lambda_cloud.ssh_keys.request") as mock:
        yield mock


# Test the LambdaCloudInstance class
class TestLambdaCloudSshKey:
    def test_add_ssh_key(self, mock_request):
        ssh = {"name": "newly-generated-key"}
        ssh_response = {
            "data": {
                "id": "0920582c7ff041399e34823a0be62548",
                "name": "newly-generated-key",
                "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfKpav4ILY54InZe27G user",
                "private_key": "null",
            }
        }
        # Mock the response
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(ssh_response).encode("utf-8")
        mock_request.return_value = mock_response

        lambda_cloud_ssh = LambdaCloudSshKey("api_key")
        result = lambda_cloud_ssh.add_ssh_key(**ssh)

        mock_request.assert_called_with(
            "POST",
            "https://cloud.lambdalabs.com/api/v1/ssh-keys",
            headers={"Authorization": "Bearer api_key"},
            json=ssh,
        )

        assert result == ssh_response

    def test_get_ssh_keys(self, mock_request):
        ssh_response = {
            "data": [
                {
                    "id": "0920582c7ff041399e34823a0be62548",
                    "name": "macbook-pro",
                    "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfKpav4ILY54InZe27G user",
                    "private_key": "null",
                }
            ]
        }

        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(ssh_response).encode("utf-8")
        mock_request.return_value = mock_response

        lambda_cloud_instance = LambdaCloudSshKey("api_key")
        result = lambda_cloud_instance.get_ssh_keys()

        mock_request.assert_called_with(
            "GET",
            "https://cloud.lambdalabs.com/api/v1/ssh-keys",
            headers={"Authorization": "Bearer api_key"},
        )
        assert result == ssh_response

    def test_delete_ssh_keys(self, mock_request):
        ssh_response = {"data": {}}

        mock_response = Response()
        mock_response.status_code = 200

        mock_response._content = json.dumps(ssh_response).encode("utf-8")
        mock_request.return_value = mock_response

        lambda_cloud_instance = LambdaCloudSshKey("api_key")
        result = lambda_cloud_instance.delete_ssh_keys(ssh_key_id="random_ssh_key_id")

        mock_request.assert_called_with(
            "DELETE",
            "https://cloud.lambdalabs.com/api/v1/ssh-keys/random_ssh_key_id",
            headers={"Authorization": "Bearer api_key"},
        )
        assert result == ssh_response
