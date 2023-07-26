import time

from lambda_cloud.base import Base
from typing import List, Dict, Any
from utilities import process_request

from requests import request


class LambdaCloudInstance(Base):
    """
    This class is used to interact with Lambda Cloud instances.
    """

    def get_instance_types(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        get instance types available on Lambda GPU Cloud, including regions in which they are available.
        :return: Returns a detailed list of the instance types offered by Lambda GPU Cloud.
        The details include the regions, if any, in which each instance type is currently available
        """
        url = f"{self.base_url}/v1/instance-types"
        results = request(
            "GET",
            url,
            headers=self.headers,
        )
        return process_request(results)

    def get_all_instances(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        get all instances associated with the user's account
        :return: Returns a list of all instances associated with the user's account.
        """
        url = f"{self.base_url}/v1/instances"
        results = request(
            "GET",
            url,
            headers=self.headers,
        )
        return process_request(results)

    def get_instance(self, instance_id: str) -> Dict[str, Dict[str, Any]]:
        """
        get a specific instance by id
        :param instance_id: unique id of the instance
        :return:
        """
        url = f"{self.base_url}/v1/instances/{instance_id}"
        results = request(
            "GET",
            url,
            headers=self.headers,
        )
        return process_request(results)

    def launch_instance(
        self,
        region_name: str,
        instance_type_name: str,
        ssh_key_names: List,
        file_system_names: List = [],
        quantity: int = [],
        name: str = None,
    ) -> Dict[str, Dict[str, List[Any]]]:
        """
        Launches one or more instances of a given instance type.
        :param region_name: Short name of a region
        :param instance_type_name: Name of an instance type
        :param ssh_key_names: Names of the SSH keys to allow access to the instances.
        Currently, exactly one SSH key must be specified.
        :param file_system_names: Names of the file systems to attach to the instances.
        Currently, only one (if any) file system may be specified
        :param quantity: Number of instances to launch
        :param name: User-provided name for the instance
        :return: Returns a list of the instances that were launched.
        """
        if not region_name or not instance_type_name or not ssh_key_names:
            raise ValueError("region, instance_type, and ssh_key_names are required")

        if not isinstance(ssh_key_names, list) or not isinstance(file_system_names, list):
            raise ValueError("ssh_key_names and file_system_names must be lists")

        if len(ssh_key_names) > 1 or len(file_system_names) > 1:
            raise ValueError("ssh_key_names and file_system_names must be lists of length 1")

        instance_details = {
            "region_name": region_name,
            "instance_type_name": instance_type_name,
            "ssh_key_names": ssh_key_names,
            "file_system_names": file_system_names,
            "quantity": quantity,
            "name": name,
        }
        if not name:
            instance_details.pop("name")
        url = f"{self.base_url}/v1/instance-operations/launch"

        rate_status_code = 429

        while rate_status_code == 429:
            results = request(
                "POST",
                url,
                headers=self.headers,
                json=instance_details,
            )
            rate_status_code = results.status_code
            if rate_status_code == 429:
                print("Too many requests. Waiting 60 seconds and trying again.")
                time.sleep(60)

        return process_request(results)

    def terminate_instance(self, instance_ids: List[str]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        terminate an instance
        :param instance_ids: an array of instance ids to terminate
        :return: a list of the instances that were terminated
        """
        url = f"{self.base_url}/v1/instance-operations/terminate"
        results = request(
            "POST",
            url,
            headers=self.headers,
            json={
                "instance_ids": instance_ids,
            },
        )
        return process_request(results)

    def restart_instance(self, instance_ids: List[str]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        restart an instance
        :param instance_ids: an array of instance ids to restart
        :return: an array detailing the instances that were restarted
        """
        url = f"{self.base_url}/v1/instance-operations/restart"
        results = request(
            "POST",
            url,
            headers=self.headers,
            json={
                "instance_ids": instance_ids,
            },
        )
        return process_request(results)
