
import os
from setuptools import setup, find_packages

ROOT = os.path.dirname(__file__)
print(f"ROOT -> {ROOT}")


setup(
    name="LangChainProjects",
    version="1.0.0",
    description="All possible LangChain projects",
    packages=find_packages(),
    include_package_data=True
)
