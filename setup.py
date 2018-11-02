from setuptools import setup, find_packages
with open('README.md') as f:
    readme = f.read()
with open('LICENSE') as f:
    license = f.read()
setup(
    name='Blue book',
    version='0.0.1',
    description='',
    long_description=readme,
    author='RachitBedi/Infrasoft',
    author_email='rachit.bedi@infrasofttech.com',
    url='',
    license=license,
    packages=find_packages()
)