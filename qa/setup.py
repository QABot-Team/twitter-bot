import os
import sys
from setuptools import setup

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(DIR + '/src')

setup(
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
