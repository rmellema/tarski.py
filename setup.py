"""
The setup script for tarski.py. Can be used to install the module in the usual way.
"""
from codecs import open
from distutils.core import setup

import tarski

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(name='tarski.py',
      # Meta data
      version=tarski.__VERSION__,
      description="Turns Tarski's World files into their formal representation",
      long_description=long_description,
      keywords='logic',
      license='MIT',

      # Author information
      author='René Mellema',
      author_email='rene.mellema@gmail.com',
      packages=['tarski'],

      # Requirements
      install_requires=[],
      extras_require={
          'dev': ['sphinx>=1.6', 'pylint>=1.7'],
          'test': ['pytest>=3'],
          },
      python_requires='~=3.4',

      classifiers=[
          'Development Status :: 1 - Planning',
          'Environment :: Console',
          'Intended Audience :: Education',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Utilities',
          ],

      # Entry points
      entry_points={
          'console_scripts': [
              'tarski = tarski.cli:main',
          ],
          'tarski.readers': [
              'tarski = tarski.read.tarski:TarskiWorldReader',
          ],
      },
     )
