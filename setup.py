from setuptools import setup, find_packages
import os

version = '1.0.0'

with open("requirements.txt", "r") as f:
	install_requires = f.readlines()

setup(
    name='frappe_ldap',
    version=version,
    description='Ldap Auth',
    author='Frappe',
    author_email='hello@frappe.io',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
