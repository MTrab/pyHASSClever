# -*- coding: utf-8 -*-

import sys

import setuptools

if sys.version_info < (3, 9, 0):
    sys.exit("The pyClever module requires Python 3.9.0 or later")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyHASSClever",
    description="Unofficial Clever Chargepoints API library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Malene Trab",
    author_email="malene@trab.dk",
    license="MIT",
    url="https://github.com/mtrab/pyHASSClever",
    packages=setuptools.find_packages(),
    project_urls={
        "Bug Tracker": "https://github.com/mtrab/pyHASSClever/issues",
    },
    install_requires=[
        "requests>=2.26.0",
    ],
)
