import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import yolk-python module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yolk'))
from version import VERSION

long_description = '''
This is the official Yolk python tracker that wraps Yolk's pipeline API.

Documentation and more details at https://github.com/yolkdata/yolk-python
'''

install_requires = [
    "requests>=2.7,<3.0",
    "six>=1.5",
    "monotonic>=1.5",
    "backoff==1.10.0",
    "python-dateutil>2.1"
]

tests_require = [
    "mock==2.0.0",
    "pylint==1.9.3",
    "flake8==3.7.9",
]

setup(
    name='yolk-python',
    version=VERSION,
    url='https://github.com/yolkdata/yolk-python',
    author='Yolk',
    author_email='engineering@yolkdata.com',
    maintainer='Yolk',
    maintainer_email='engineering@yolkdata.com',
    test_suite='yolk.test.all',
    packages=['yolk', 'yolk.test'],
    license='MIT License',
    install_requires=install_requires,
    extras_require={
        'test': tests_require
    },
    description='The hassle-free way to integrate Yolk into any python application.',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
