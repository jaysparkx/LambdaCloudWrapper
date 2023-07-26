import sys
import time

from lambda_cloud.instances import LambdaCloudInstance
from lambda_cloud.ssh_keys import LambdaCloudSshKey
from lambda_cloud.file_systems import LambdaCloudFileSystem

import random


def create_objects(token):
    lambda_instances = LambdaCloudInstance(token=token)
    lambda_ssh = LambdaCloudSshKey(token=token)
    lambda_file_systems = LambdaCloudFileSystem(token=token)

    num_1 = random.randint(0, 100)
    num_2 = random.randint(50, 100)

    print("creating ssh key with name taiwo_test_key")
    new_ssh_key_name = f"test_key_{num_1}_{num_2}"
    new_ssh_key = lambda_ssh.add_ssh_key(name=new_ssh_key_name)
    new_ssh_key_id = new_ssh_key["data"]["id"]
    print(f"created ssh key `{new_ssh_key_name}` with id", new_ssh_key_id)

    # list all existing instances
    print("listing all existing instances: ")
    all_existing_instances = lambda_instances.get_all_instances()
    new_instances = []
    if len(all_existing_instances["data"]) == 0:
        print("no instances found")
    else:
        for _instance in all_existing_instances["data"]:
            print(f"* {_instance['name']}")

    # get available types
    print("getting available instance types")
    instances_availability = lambda_instances.get_instance_types()
    instances_availability = instances_availability["data"]

    for instance_type in instances_availability:
        instance_details = instances_availability[instance_type]
        if len(instance_details["regions_with_capacity_available"]) > 0:
            print(f"creating instance of type {instance_details['instance_type']['name']}")
            instance_config = {
                "region_name": instance_details["regions_with_capacity_available"][0]["name"],
                "instance_type_name": instance_details["instance_type"]["name"],
                "ssh_key_names": [new_ssh_key_name],
                "quantity": 1,
                "name": f"test_instance_{num_1}_{num_2}",
            }
            new_instance = lambda_instances.launch_instance(**instance_config)
            new_instance_id = new_instance["data"]["instance_ids"][0]
            new_instances.append(new_instance_id)

            print("created instance with id", new_instance_id)

    # list all ssh keys
    print("listing all ssh keys")
    all_ssh_keys = lambda_ssh.get_ssh_keys()
    for _key in all_ssh_keys["data"]:
        print(f"\t* {_key['name']}")

    # list all file systems
    print("listing all file systems: ")
    all_file_systems = lambda_file_systems.get_file_systems()
    for _file in all_file_systems["data"]:
        print(f"\t* {_file['name']}")

    # restart instance
    print("waiting for instances to be ready before restarting")
    time.sleep(60)
    print("restarting the new instances created")
    lambda_instances.restart_instance(instance_ids=new_instances)
    print("instances restarted")

    # terminate instance
    print("waiting for 60 secs before terminating instances")
    time.sleep(60)
    lambda_instances.terminate_instance(instance_ids=new_instances)
    print("new instances terminated")

    # delete ssh key
    print("deleting ssh key with id", new_ssh_key_id)
    lambda_ssh.delete_ssh_keys(ssh_key_id=new_ssh_key_id)
    print("ssh key deleted")


if __name__ == "__main__":
    api_token = sys.argv[1]
    create_objects(api_token)
