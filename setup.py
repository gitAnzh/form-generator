import os

from setuptools import setup

requirements_dir = f"{os.getcwd()}/requirements.txt"
with open(requirements_dir, "r") as f:
    file = f.readlines()
    requirements = [line.rstrip() for line in file]

setup(
    name='form_generator',
    version='0.1.0',
    license='None',
    author='evolveZenith',
    author_email='mohsen.u3fi@hotmail.com',
    load_description=open('README.md').read(),
    packages=["source"],
    install_requires=requirements,
    zip_safe=False
)
