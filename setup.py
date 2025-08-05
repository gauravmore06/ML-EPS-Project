from setuptools import find_packages, setup
from typing import List


def get_requirements() -> list[str]:

    requirements_list = list[str] = []

    return requirements_list



setup(
name= 'sensor',
version= '0.0.1',
author= 'Gaurav',
author_email= 'gauravmore0206@gmai.com',
packages= find_packages(),
install_requires = get_requirements() #["pymongo"]



)