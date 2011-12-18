#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

from setuptools import setup

setup(
    name='Dynamics:GP 10',
    version='1.0',
    packages=['gp10'],
    author='John Hampton',
    description='SQLAlchemy table definitions for Dynamics:GP 10',
    url='https://pacopablo.com/wiki/Dev/GP10',
    license='BSD',
    zip_safe=False,
    install_requires = ['SQLAlchemy>=0.5.0rc2'],
)

