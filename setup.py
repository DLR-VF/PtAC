
"""
PtAC setup script.

See license in LICENSE.md
"""

from setuptools import setup


def readme():
    with open("ptac/README.md") as f:
        return f.read()


setup(
    name="ptac",
    version="0.1.1a",
    author="Simon Nieland, Serra Yosmaoglu",
    author_email="Simon.Nieland@dlr.de, Serra.Yosmaoglu@dlr.de",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DLR-VF/PtAC",
    # platforms="any",
    packages=["ptac", "ptac.urmoacjar"],
    include_package_data=True,
    # python_requires=">=3.8",
    # install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
    ],
)
