"""
PtAC setup script.

See license in LICENSE.txt
"""

from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()
setup(
        name='ptac',
        version='0.0.3',
        author="Simon Nieland, Serra Yosmaoglu",
        author_email="Simon.Nieland@dlr.de, Serra.Yosmaoglu@dlr.de",
        long_description=readme(),
        long_description_content_type='text/markdown',
        url='https://gitlab.dlr.de/trak-mud/ptac',
        classifiers=[
            'Development Status :: 5 - Production/Stable', 
            'Programming Language :: Python :: 3', 
            'Operating System :: OS Independent'
            #'License :: OSI Approved :: MIT License'
            ],
        licence='',
        include_package_data=True,
        packages=find_packages(exclude=['test']), #['ptac'],
        install_requires=[],
        zip_safe=False)
