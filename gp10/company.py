# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com

# Standard library imports
from datetime import datetime, date
from decimal import Decimal

# Third Party imports
from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relation
from sqlalchemy.ext.associationproxy import association_proxy

# Local imports
from gp10 import Base, get_session
from gp10.types import StripString
from gp10.util import get_next_note_index, gp_cur_date


class SY_Posting_Account_MSTR(Base):
    """ Posting Account Master """
    __tablename__ = 'SY01100'

    series = Column('SERIES', Integer, primary_key=True, autoincrement=False)
    seq = Column('SEQNUMBR', Integer, primary_key=True, autoincrement=False)
    actidx = Column('ACTINDX', Integer, nullable=False)

    def __init__(self, series, seq, actidx, **kwargs):
        self.series = series
        self.seq = seq
        self.actidx = actidx

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class Batch_Headers_DUP(Base):
    """ Posting Definitions Master Dup """
    __tablename__ = 'SY00500'

    batchsrc = Column('BCHSOURC', StripString(15), primary_key=True, default="Rcvg Trx Entry")
    batchnum = Column('BACHNUMB', StripString(15), primary_key=True)
    glpostdate = Column('GLPOSTDT', DateTime, nullable=False, default=gp_cur_date)
    series = Column('SERIES', Integer, nullable=False, default=4)
    numtrxs = Column('NUMOFTRX', Integer, nullable=False, default=1)
    batchfreq = Column('BACHFREQ', Integer, nullable=False, default=1)
    uid = Column('USERID', StripString(15), nullable=False, default='sa')
    checkbook_id = Column('CHEKBKID', StripString(15), nullable=False, default='UBOC')
    total = Column('BCHTOTAL', Numeric(19,5), nullable=False, default=Decimal(0))
    modified = Column('MODIFDT', DateTime, nullable=False, default=gp_cur_date)
    created = Column('CREATDT', DateTime, nullable=False, default=gp_cur_date)
    origin = Column('ORIGIN', Integer, nullable=False, default=1)
    noteidx = Column('NOTEINDX', Numeric(19,5), nullable=False, default=get_next_note_index)

    def __init__(self, batchnum,  **kwargs):
        self.batchnum = batchnum

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass

