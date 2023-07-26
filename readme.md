# Lambda Cloud API wrapper for Python
This is a Python wrapper for the Lambda Cloud API. documentation can be found [here](https://cloud.lambdalabs.com/api/v1/docs#).


## Getting Started
### Prerequisites
* Python 3.7 or higher
* Token required from lambda cloud console

### Modules
Each module is a different part of the API. The modules are:
* Instances
* File Systems
* SSH Keys

To use a module, import it like so:
```python
from lambda_cloud.instances import LambdaCloudInstance

token = "token gotten from lambda cloud console"
instance = LambdaCloudInstance(token)

# Do stuff with instance
all_instance = instance.get_all_instances()
print(all_instance)
```

### Testing
To run the tests, run the following command:
```bash
pytest tests
```
NB: Ensure you are the in the project root directory when running the command.

The tests validate the following:
* Every method calls the correct endpoint
* Response matches the expected response from the API

Run the command below to create test objects in Lambda Cloud:
```bash
python test_automation.py <token>
```

<token> is the secret token gotten from the Lambda Cloud console.
