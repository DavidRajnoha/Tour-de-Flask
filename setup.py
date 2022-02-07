from setuptools import find_packages, setup

setup(
    name='tourdeflask',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,  # includes also the schema.sql file
    zip_safe=False,
    install_requires=[
        'flask',
        'gunicorn'
    ],
)