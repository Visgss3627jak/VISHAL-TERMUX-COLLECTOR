from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="vishal",
    version="2.0.0",
    author="VISHAL",
    author_email="vishal@termux.com",
    description="Advanced Termux File Collection Module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vishal/termux-collector",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)