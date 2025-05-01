from setuptools import setup, find_packages

setup(
    name="getDataFromGeosphere",  # Name of your package
    version="1.0.0",
    description="A package for fetching meteorological data from Geosphere AT",
    author="Dieter Riegler",
    author_email="dieter@garageland.at",
    packages=find_packages(),  # Automatically find package directories
    install_requires=[
        "requests",
        "pandas"
    ],
    python_requires=">=3.6",
)
