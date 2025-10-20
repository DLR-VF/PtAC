#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""PtAC setup script.

See license in LICENSE.md
"""
# ===========================================================================
__author__ = "Serra Yosmaoglu, Simon Nieland, Daniel Krajzewicz"
__copyright__ = "Copyright 2021-2025, German Aerospace Center (DLR), Institute of Transport Research"
__license__ = "EPL2.0"
__version__ = "0.2.0"
__maintainer__ = "Simon Nieland"
__email__ = "simon.nieland@dlr.de"
__status__ = "Production"
# ===========================================================================
# - https://github.com/DLR-VF/PtAC
# - http://www.dlr.de/vf
# ===========================================================================

# --- imports ---------------------------------------------------------------
import os

from setuptools import setup


# --- functions -------------------------------------------------------------
def readme():
    """Read the readme file."""
    with open("README.md") as f:
        return f.read()


# only specify install_requires if not in RTD environment
if os.getenv("READTHEDOCS") == "True":
    INSTALL_REQUIRES = []
else:
    with open("requirements.txt") as f:
        INSTALL_REQUIRES = [line.strip() for line in f.readlines()]

setup(
    name="ptac",
    version="0.1.3a",
    author="Simon Nieland, Serra Yosmaoglu, Daniel Krajzewicz",
    author_email="Simon.Nieland@dlr.de, Serra.Yosmaoglu@dlr.de, Daniel.Krajzewicz@dlr.de",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DLR-VF/PtAC",
    platforms="any",
    packages=["ptac", "ptac.urmoacjar"],
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
    ],
)
