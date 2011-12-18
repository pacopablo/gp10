# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

# Standard library imports
from datetime import datetime, date
from decimal import Decimal

# Third Party imports
from sqlalchemy import Column

# Local imports
from gp10 import Base
from gp10.types import StripString

class MC_SETP(Base):
    """ Multicurrency Setup """
    __tablename__ = 'MC40000'

    currency = Column('FUNLCURR', StripString(15), primary_key=True)

    def __init__(self, currency, **kwargs):
        self.currency = currency

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass
