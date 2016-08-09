# setup.py
# -*- coding: utf-8 -*-

from setuptools import setup
from distutils.util import convert_path

def readme():
    with open('README.rst') as f:
        return f.read()

version = {}
with open(convert_path('grm/__version__.py')) as f:
    exec(f.read(), version)

__gh = 'https://github.com/btskinner/'
__nm = 'grm'

setup(name='{}'.format(__nm),
      version=version['__version__'],
      description='GitHub classroom manager',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='github organization classroom manager',
      url='https://github.com/btskinner/grm',
      download_url='{}{}/archive/v{}.tar.gz'.format(__gh, __nm, version['__version__']),
      author='Benjamin Skinner',
      author_email='b.skinner@vanderbilt.edu',
      license='MIT',
      packages=['grm'],
      install_requires=[
          'pandas',
          'requests',
      ],
      scripts=['bin/gitroom'],
      zip_safe=False)
