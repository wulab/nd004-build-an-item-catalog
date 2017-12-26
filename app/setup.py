from setuptools import setup

setup(
    name='ItemCatalog',
    packages=['itemcatalog'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'Jinja2'
    ],
)
