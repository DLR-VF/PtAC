from setuptools import setup, find_packages
#import pathlib

#here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
#long_description = (here / 'README.md').read_text(encoding='utf-8')
def readme():
    with open('README.md') as f:
        return f.read()
setup(
        name='ptac',
        version='0.0.1', 
        long_description=readme(),
        long_description_content_type='text/markdown',
        url='https://gitlab.dlr.de/trak-mud/ptac',
        classifiers=[
            'Development Status :: 5 - Production/Stable', 
            'Programming Language :: Python :: 3', 
            'Operating System :: OS Independent', 
            'License :: OSI Approved :: MIT License'
            ],
        licence='MIT', 
        packages=find_packages(exclude=['test']), #['ptac'], #
        install_requires=[], 
        include_package_data=True,
        zip_safe=False)
        
