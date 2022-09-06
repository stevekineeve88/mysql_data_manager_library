import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mysql_data_manager",
    version="0.0.1",
    author="Stephen Ayre",
    author_email="stevemamajama@gmail.com",
    description="MySQL data manager wrapper for mysql-connector-python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stevekineeve88/mysql_data_manager_library.git",
    packages=setuptools.find_packages(),
    install_requires=[
        "mysql-connector-python==8.0.30"
    ],
    python_requires='>=3.7'
)
