from setuptools import find_packages, setuptools

setup(
    name='Paidin',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'switchfx',
        ],
)