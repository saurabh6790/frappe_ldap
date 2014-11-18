from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='frappe_ldap',
    version=version,
    description='Ldap Auth',
    author='New Indictrnas',
    author_email='saurabh.p@indinctranstech.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
