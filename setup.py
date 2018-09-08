import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="azure_automation_utility",
    version="0.0.1",
    author="Azure Automation Team",
    author_email="scorch@microsoft.com",
    description="Utilities to make it easier to perform common tasks from Azure Automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azureautomation/azure_automation_utility",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)