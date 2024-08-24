# Uploading package to PyPi.

from setuptools import setup

with open('README.rst', 'r') as fh:
      long_description = fh.read()

setup(name='schoolopy',
      version='0.3.2',
      description='A Python wrapper for Schoology\'s API.',
      long_description=long_description,
      url='https://github.com/ErikBoesen/schoolopy',
      author='Erik Boesen',
      author_email='me@erikboesen.com',
      license='MIT',
      packages=['schoolopy'],
      install_requires=['requests', 'requests-oauthlib', 'oauthlib'],
      zip_safe=False)
