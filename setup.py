
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='grm',
      version='0.1',
      description='GitHub classroom manager',
      long_description=readme(),
      classifiers=[
          'Programming Language :: Python :: 3.5',
      ],
      keywords='github organization classroom manager',
      url='https://github.com/btskinner/grm',
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
