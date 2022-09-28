from setuptools import setup

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()


setup(
    name="osrsutils",
    author='Flailfish',
    url='https://github.com/Flailfish/osrsutils',
    version="1.0",
    install_requires=requirements,
    description = 'API wrapper for osrs wiki api and osrs index_lite',
    python_requires='>=3.7.0',
    packages = ['osrsutils'],
    include_package_data=True
)
