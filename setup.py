from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # Package name:
    name="ml_project",

    # Package number (initial):
    version="0.1.0",

    # Package author details:
    author="Jorge Rivero Dones",
    author_email="jorivero83@gmail.com",

    # Packages
    packages=["ml_project"],

    # Include additional files into the package
    include_package_data=False,

    # Details
    url="https://github.com/jorivero83/ml_project",

    #
    # license="LICENSE.txt",
    description="Example of ML project",

    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',

    # Dependent packages (distributions)
    install_requires=[
        'bme==0.1.0',
        'scikit-learn==1.0.2',
        'lightgbm==3.3.3'
    ],
)