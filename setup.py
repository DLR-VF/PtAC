"""
PtAC setup script.

See license in LICENSE.txt
"""

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


if __name__ == "__main__":
    setup()
# setup(
#         name="ptac",
#         version="0.0.6",
#         author="Simon Nieland, Serra Yosmaoglu",
#         author_email="Simon.Nieland@dlr.de, Serra.Yosmaoglu@dlr.de",
#         long_description=readme(),
#         long_description_content_type='text/markdown',
#         url="https://github.com/DLR-VF/PtAC",
#         classifiers=[
#             'Development Status :: 5 - Production/Stable',
#             'Programming Language :: Python :: 3',
#             'Operating System :: OS Independent',
#             'License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)'
#             ],
#         licence="Eclipse Public License 2.0 (EPL-2.0)",
#         include_package_data=True,
#         packages=find_packages(exclude=["test"]),
#         zip_safe=False)
