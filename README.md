# Azure Automation utility package

Contains a python package to make it easier to author Python within Azure Automation.
It contains the following functions:

* get_automation_runas_credential()
* get_automation_runas_token()
* import_child_runbook(resource_group, automation_account, runbook_name)
* load_webhook_body()

## Build instructions

You can create a wheel file by following the below steps

* Download or clone this repository.
* Run the below commands to create the package and install using pip.

```bash
python setup.py sdist bdist_wheel
pip install .
```

## Example usage

### List resource groups

```python
import azure.mgmt.resource
import automationassets
from azure_automation_utility import get_automation_runas_credential

# Authenticate to Azure using the Azure Automation RunAs service principal
runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
azure_credential = get_automation_runas_credential()

# Intialize the resource management client with the RunAs credential and subscription
resource_client = azure.mgmt.resource.ResourceManagementClient(
    azure_credential,
    str(runas_connection["SubscriptionId"]))

# Get list of resource groups and print them out
groups = resource_client.resource_groups.list()
for group in groups:
    print group.name
```

### Call a function in a child runbook

```python
from azure_automation_utility import import_child_runbook

# Import child runbook and call some function
child_runbook = import_child_runbook("ContosoGroup", "ContosoAccount", "hello_world")

# hello_world runbook that is published in the Automation account
"""
# #!/usr/bin/env python2
# def hello(name):
    print ("Hello " + name)
"""

child_runbook.hello("world")
```

### Get webhook request body

```python
from azure_automation_utility import load_webhook_body

requestBody = load_webhook_body()
print requestBody
```
