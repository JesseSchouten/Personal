from glob import glob
from os.path import splitext
from os.path import basename

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jesse", 
    version="0.0.0",
    url = "https://github.com/DutchChannels/analytics-tier.git",
    author="Jesse Schouten",
    author_email="jesse.schouten@outlook.com",
    description="Test function to test github actions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages('src/lib'),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
    install_requires=[
    ]
)