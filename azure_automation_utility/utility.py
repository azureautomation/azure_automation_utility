
# Returns a credential based on an Azure Automation RunAs connection dictionary
def get_automation_runas_credential():
    """ Returs a credential that can be used to authenticate against Azure resources """
    from OpenSSL import crypto
    from msrestazure import azure_active_directory
    import adal
    import automationassets

    # Get the Azure Automation RunAs service principal certificate
    runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
    cert = automationassets.get_automation_certificate("AzureRunAsCertificate")
    sp_cert = crypto.load_pkcs12(cert)
    pem_pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, sp_cert.get_privatekey())

    # Get run as connection information for the Azure Automation service principal
    application_id = runas_connection["ApplicationId"]
    thumbprint = runas_connection["CertificateThumbprint"]
    tenant_id = runas_connection["TenantId"]

    # Authenticate with service principal certificate
    resource = "https://management.core.windows.net/"
    authority_url = ("https://login.microsoftonline.com/" + tenant_id)
    context = adal.AuthenticationContext(authority_url)
    return azure_active_directory.AdalAuthentication(
        lambda: context.acquire_token_with_client_certificate(
            resource,
            application_id,
            pem_pkey,
            thumbprint)
    )

# Return token based on Azure automation Runas connection
def get_automation_runas_token():
    """ Returs a token that can be used to authenticate against Azure resources """
    from OpenSSL import crypto
    import adal
    import automationassets

    # Get the Azure Automation RunAs service principal certificate
    cert = automationassets.get_automation_certificate("AzureRunAsCertificate")
    sp_cert = crypto.load_pkcs12(cert)
    pem_pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, sp_cert.get_privatekey())

    # Get run as connection information for the Azure Automation service principal
    runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
    application_id = runas_connection["ApplicationId"]
    thumbprint = runas_connection["CertificateThumbprint"]
    tenant_id = runas_connection["TenantId"]

    # Authenticate with service principal certificate
    resource = "https://management.core.windows.net/"
    authority_url = ("https://login.microsoftonline.com/" + tenant_id)
    context = adal.AuthenticationContext(authority_url)
    azure_credential = context.acquire_token_with_client_certificate(
        resource,
        application_id,
        pem_pkey,
        thumbprint)

    # Return the token
    return azure_credential.get('accessToken')

def import_child_runbook(resource_group, automation_account, runbook_name):
    """ Downloads a runbook from the automation account to the cloud container """
    import os
    import sys
    import requests
    import automationassets

    # Get RunAs access token
    access_token = get_automation_runas_token()

    # Set what resources to act against
    runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
    subscription_id = str(runas_connection["SubscriptionId"])

    # Set up URI to create a new automation job
    uri = ("https://management.azure.com/subscriptions/" + subscription_id
           + "/resourceGroups/" + resource_group
           + "/providers/Microsoft.Automation/automationAccounts/" + automation_account
           + "/runbooks/" + runbook_name + "/content?api-version=2015-10-31")


    # Make request to get runbook content
    headers = {"Authorization": 'Bearer ' + access_token}
    result = requests.get(uri, headers=headers)

    runbookfile = os.path.join(sys.path[0], runbook_name) + ".py"

    with open(runbookfile, "w") as text_file:
        text_file.write(result.text)
    
    # Import downloaded python module and return to caller
    import importlib
    return importlib.import_module(runbook_name)
    
def load_webhook_body():
    """ Parses the arguments sent in from a webhook and returns the request body as a python object """
    import sys
    import json

    # Read all the arguments sent in by the webhook
    payload = ""
    for index in range(len(sys.argv)):
        payload += str(sys.argv[index]).strip()

    # Get the RequestBody so we can process it
    start = payload.find("RequestBody:")
    end = payload.find("RequestHeader:")
    requestBody = payload[start+12:end-1]

    # return webhook request body as Python dictionary
    return json.loads(str(requestBody))

