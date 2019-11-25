import os

from setuptools import find_packages
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="drf-link-navigation-pagination",
    version="0.0.4",
    description="Yet another pagination class for DRF to set host address by header",
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    author="Willian Antunes",
    author_email="Willian Antunes <willian.lima.antunes@gmail.com>",
    license="MIT",
    url="https://github.com/juntossomosmais/drf-link-navigation-pagination",
    packages=find_packages(),
    install_requires=["django", "djangorestframework"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Framework :: Django :: 2.2",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
