#!/usr/bin/env python
# coding: utf-8

r"""ydeos_parallel's setup.py"""

import ydeos_parallel
from distutils.core import setup

setup(name=ydeos_parallel.__name__,
      version=ydeos_parallel.__version__,
      description=ydeos_parallel.__description__,
      long_description='Code parallelization',
      url=ydeos_parallel.__url__,
      download_url=ydeos_parallel.__download_url__,
      author=ydeos_parallel.__author__,
      author_email=ydeos_parallel.__author_email__,
      license=ydeos_parallel.__license__,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7'],
      keywords='parallelization',
      packages=['ydeos_parallel'])
