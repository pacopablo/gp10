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
from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relation
from sqlalchemy.ext.associationproxy import association_proxy

# Local imports
from gp10 import Base, get_session
from gp10.util import gp_cur_date
from gp10.types import StripString, Ordinal

__all__ = [
    'SOP_LINE_WORK',
    'SOP_Serial_Lot_WORK_HIST',
]

class SOP_LINE_WORK(Base):
    """ Sales Transaction Amounts Work """
    __tablename__ = 'SOP10200'

    soptype = Column('SOPTYPE', Integer, primary_key=True, default=1)
    sopnum = Column('SOPNUMBE', StripString(21), primary_key=True)
    lineitemseq = Column('LNITMSEQ', Integer, primary_key=True, default=Ordinal(0))
    componentseq = Column('CMPNTSEQ', Integer, primary_key=True, default=0)
    item = Column('ITEMNMBR', StripString(31), ForeignKey('IV00101.ITEMNMBR'), nullable=False)
    location = Column('LOCNCODE', StripString(11), nullable=False, default='PCSF')
    qty = Column('QUANTITY', Numeric(19,5), nullable=False, default=0)
    qtyallocated = Column('ATYALLOC', Numeric(19,5), nullable=False, default=0)

    def __init__(self, sopnum, item, **kwargs):
        self.sopnum = sopnum
        self.item = item

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class SOP_Serial_Lot_WORK_HIST(Base):
    """ Sales Serial/Lot Work and History """
    __tablename__ = 'SOP10201'
    __table_args__ = (ForeignKeyConstraint(['SOPTYPE',
                                            'SOPNUMBE',
                                            'LNITMSEQ',
                                            'CMPNTSEQ',
                                            'ITEMNMBR'],
                                           ['SOP10200.SOPTYPE',
                                            'SOP10200.SOPNUMBE',
                                            'SOP10200.LNITMSEQ',
                                            'SOP10200.CMPNTSEQ',
                                            'SOP10200.ITEMNMBR']), {})

    soptype = Column('SOPTYPE', Integer, primary_key=True, default=1)
    sopnum = Column('SOPNUMBE', StripString(21), primary_key=True)
    lineitemseq = Column('LNITMSEQ', Integer, primary_key=True, default=Ordinal(0))
    componentseq = Column('CMPNTSEQ', Integer, primary_key=True, default=0)
    qtytype = Column('QTYTYPE', Integer, primary_key=True, default=1)
    lotseq = Column('SLTSQNUM', Integer, primary_key=True, default=Ordinal(0))
    received = Column('DATERECD', DateTime, primary_key=True, default=gp_cur_date)
    dateseq = Column('DTSEQNUM', Integer, primary_key=True, autoincrement=False, default=Decimal(1))
    lot = Column('SERLTNUM', StripString(21), nullable=False)
    qty = Column('SERLTQTY', Numeric(19,5), nullable=False, default=0)
    item = Column('ITEMNMBR', StripString(31), ForeignKey('IV00101.ITEMNMBR'), nullable=False)
    posted = Column('POSTED', Integer, nullable=False, default=0)


    def __init__(self, sopnum, item, lot, **kwargs):
        self.sopnum = sopnum
        self.item = item
        self.lot = lot

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass
