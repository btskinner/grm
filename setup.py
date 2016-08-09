# setup.py
# -*- coding: utf-8 -*-

from setuptools import setup
from distutils.util import convert_path

def readme():
    with open('README.rst') as f:
        return f.read()

info = {}
with open(convert_path('grm/__info__.py')) as f:
    exec(f.read(), info)

setup(name=info['__nm'],
      version=info['__version__'],
      description='GitHub classroom manager',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='github organization classroom manager',
      url=info['__rp'],
      download_url=info['__dl'],
      author=info['__au'],
      author_email=info['__em'],
      license='MIT',
      packages=['grm'],
      install_requires=[
          'pandas',
          'requests',
      ],
      scripts=['bin/gitroom'],
      zip_safe=False)
