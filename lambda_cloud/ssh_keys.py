from lambda_cloud.base import Base
from typing import List, Dict, Optional
from utilities import process_request

from requests import request


class LambdaCloudSshKey(Base):
    """
    This class is used to interact with Lambda Cloud ssh keys.
    """

    def add_ssh_key(self, name: str, public_key: str = None) -> Dict[str, Dict[str, str]]:
        """
        add an ssh key.
        To use an existing key pair, input the public_key.
        To generate a new key pair, omit the public_key. Save the private_key from the response somewhere secure
        :param name: name of the ssh key
        :param public_key: Public key for the SSH key
        :return: details of the ssh key
        """
        url = f"{self.base_url}/v1/ssh-keys"
        payload = {
            "name": name,
            "public_key": public_key,
        }

        if not public_key:
            payload.pop("public_key")

        results = request(
            "POST",
            url,
            headers=self.headers,
            json=payload,
        )
        return process_request(results)

    def delete_ssh_keys(self, ssh_key_id) -> Optional:
        """
        delete an ssh key
        :param ssh_key_id:
        :return:
        """
        url = f"{self.base_url}/v1/ssh-keys/{ssh_key_id}"
        results = request(
            "DELETE",
            url,
            headers=self.headers,
        )
        return process_request(results)

    def get_ssh_keys(self) -> Dict[str, List[Dict[str, str]]]:
        """
        get all ssh keys associated with the user's account
        :return: Returns a list of all ssh keys associated with the user's account.
        """
        url = f"{self.base_url}/v1/ssh-keys"
        results = request(
            "GET",
            url,
            headers=self.headers,
        )
        return process_request(results)
