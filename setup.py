import os
import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

with open("requirements.txt", "r") as file:
    requirements = file.read().strip().split("\n")

setuptools.setup(
    name="python-arduino",
    version="0.0.1",
    author="Patrick Huang",
    author_email="huangpatrick16777216@gmail.com",
    description="An API for controlling Arduino boards.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phuang1024/python-arduino",
    py_modules=["arduino"],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
