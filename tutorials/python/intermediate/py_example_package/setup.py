from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='mypackage',
    version='0.0.1',    
    description='A simple Python package.',
    url='',
    author='Umberto Grando',
    author_email='grando.umberto@gmail.com',
    license='MIT',
    packages=['mypackage'],
    install_requires=required,
    package_data={'': ['data/*.txt']},
    include_package_data=True,
)