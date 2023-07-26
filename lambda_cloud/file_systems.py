from lambda_cloud.base import Base
from typing import List, Dict, Any
from utilities import process_request

from requests import request


class LambdaCloudFileSystem(Base):
    """
    This class is used to interact with Lambda Cloud file systems.
    """

    def get_file_systems(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retrieve the list of file systems
        :return: Returns a list of all file systems associated with the user's account.
        """
        url = f"{self.base_url}/v1/file-systems"
        results = request(
            "GET",
            url,
            headers=self.headers,
        )
        return process_request(results)
