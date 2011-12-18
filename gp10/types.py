# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

# Standard library imports

# Third Party imports
import sqlalchemy.types as saTypes

# Local imports
from gp10.util import to_ord, from_ord

__all__ = [
    'StripString',
    'Ordinal',
]

class StripString(saTypes.TypeDecorator):
    impl = saTypes.String

    def process_result_value(self, value, dialect):
        return value.strip()

    def copy(self):
        return StripString(self.impl.length)


class Ordinal(saTypes.TypeDecorator):
    impl = saTypes.Integer

    def process_result_value(self, value, dialect):
        return from_ord(value)

    def process_bind_param(self, value, dialect):
        return to_ord(value)
