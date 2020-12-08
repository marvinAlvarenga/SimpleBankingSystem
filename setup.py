import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-banking-system",
    version="1.0.1",
    author="Marvin Alvarenga",
    author_email="marvinalexz@gmail.com",
    description="A simple use of design patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marvinAlvarenga/SimpleBankingSystem",
    packages=setuptools.find_packages(),
    scripts=['run.py'],
)
