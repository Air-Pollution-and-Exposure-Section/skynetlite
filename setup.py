#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="skynet",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "arrow==1.2.3",
        "psycopg2-binary==2.9.9",
        "requests==2.29.0",
        "sqlalchemy==2.0.25",
        "pandas",
        "pytest",
    ],
)
