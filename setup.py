from setuptools import setup,find_packages
from typing import List



def get_requirement()->list[str]:

    requirement_list:List[str] = []
    try:
        with open("requirement.txt", "r") as f:
            lines = f.readlines()

            for i in lines:
                requirement = i.strip()

                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)

    except FileNotFoundError:
        print('file not found ....')

    return requirement_list

# print(get_requirement())
setup(
    name="URL Validation",
    version="1.0.0",
    author="Aman Kumar Choudhary",
    author_email="amankumarchy5423@gmail.com",
    packages= find_packages(),
    install_requires=get_requirement(),

)
