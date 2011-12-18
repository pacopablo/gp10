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
from gp10.types import StripString, Ordinal
from gp10.util import get_session, get_next_note_index, gp_cur_date
from gp10.util import gp_cur_time, gp_epoch_start

def get_currency():
    return 'Z-US$'

class IV_Item_MSTR(Base):
    """ Item Master """
    __tablename__ = 'IV00101'

    item = Column('ITEMNMBR', StripString(31), primary_key=True)
    itemdesc = Column('ITEMDESC', StripString(101), nullable=False)
    shortname = Column('ITMSHNAM', StripString(15), nullable=False)
    itemtype = Column('ITEMTYPE', Integer, nullable=False, default=1)
    stdcost = Column('STNDCOST', Numeric(19,5), nullable=False)
    curcost = Column('CURRCOST', Numeric(19,5), nullable=False)
    dec_places_qtys = Column('DECPLQTY', Integer, nullable=False, default=1)
    dec_places_curr = Column('DECPLCUR', Integer, nullable=False, default=3)
    itemtracking = Column('ITMTRKOP', Integer, nullable=False, default=3)
    itemclass = Column('ITMCLSCD', StripString(11), nullable=False, default='MAIN')
    uofmschedule = Column('UOMSCHDL', StripString(11), nullable=False, default='EACH')
    alternate1 = Column('ALTITEM1', StripString(31), nullable=False, default='')
    alternate2 = Column('ALTITEM2', StripString(31), nullable=False, default='')
    usercategory1 = Column('USCATVLS_1', StripString(11), nullable=False, default='')
    usercategory2 = Column('USCATVLS_2', StripString(11), nullable=False, default='')
    usercategory3 = Column('USCATVLS_3', StripString(11), nullable=False, default='')
    usercategory4 = Column('USCATVLS_4', StripString(11), nullable=False, default='')
    usercategory5 = Column('USCATVLS_5', StripString(11), nullable=False, default='')
    usercategory6 = Column('USCATVLS_6', StripString(11), nullable=False, default='')
    location = Column('LOCNCODE', StripString(11), nullable=False)
    invactindx = Column('IVIVINDX', Integer, nullable=False, default=147)

    def __init__(self, item, itemdesc, shortname, stdcost, location, **kwargs):
        self.item = item
        self.itemdesc = itemdesc
        self.shortname = shortname
        self.stdcost = stdcost
        self.curcost = self.stdcost
        self.location = location

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class IV_Item_MSTR_QTYS(Base):
    """ Item Quantity Master """
    __tablename__ = 'IV00102'

    item = Column('ITEMNMBR', StripString(31), ForeignKey('IV00101'), primary_key=True)
    location = Column('LOCNCODE', StripString(11), primary_key=True)
    recordtype = Column('RCRDTYPE', Integer, primary_key=True, autoincrement=False, default=2)
    bin = Column('BINNMBR', StripString(21), nullable=False, default='')
    qtyonhand = Column('QTYONHND', Numeric(19,5), nullable=False, default=0)
    qtyallocated = Column('ATYALLOC', Numeric(19,5), nullable=False, default=0)
    qtysold = Column('QTYSOLD', Numeric(19,5), nullable=False, default=0)
    landed_cost_id = Column('Landed_Cost_Group_ID', StripString(15), nullable=False, default='')
    orderpolicy = Column('ORDERPOLICY', Integer, nullable=False, default=1)
    numdays = Column('NMBROFDYS', Integer, nullable=False, default=1)
    ordermultiple = Column('ORDERMULTIPLE', Numeric(19,5), nullable=False, default=1.0)
    replenishmethod = Column('REPLENISHMENTMETHOD', Integer, nullable=False, default=3)
    includeplanning = Column('INCLDDINPLNNNG', Integer, nullable=False, default=1)
    forcast_consumption_period = Column('FRCSTCNSMPTNPRD', Integer, nullable=False, default=3)
    replenishlevel = Column('ReplenishmentLevel', Integer, nullable=False, default=1)
    ordermethod = Column('POPOrderMethod', Integer, nullable=False, default=1)
    vendorselection = Column('POPVendorSelection', Integer, nullable=False, default=1)
    pricingselection = Column('POPPricingSelection', Integer, nullable=False, default=1)
    includeallocations = Column('IncludeAllocations', Integer, nullable=False, default=1)
    includebackorders = Column('IncludeBackorders', Integer, nullable=False, default=1)
    includerequisitions = Column('IncludeRequisitions', Integer, nullable=False, default=1)
    pick_ticket_option = Column('PICKTICKETITEMOPT', Integer, nullable=False, default=3)
    mrpmovein = Column('INCLDMRPMOVEIN', Integer, nullable=False, default=1)
    mrpmoveout = Column('INCLDMRPMOVEOUT', Integer, nullable=False, default=1)
    mrpcancel = Column('INCLDMRPCANCEL', Integer, nullable=False, default=1)

    def __init__(self, item, location, **kwargs):
        self.item = item
        self.location = location

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass

    def _available(self):
        return self.qtyonhand - (self.qtyallocated >= 0 and self.qtyallocated or 0) - self.qtysold
    available = property(_available)


class IV_Lot_MSTR(Base):
    """ Item Lot Number Master """
    __tablename__ = 'IV00300'

    item = Column('ITEMNMBR', StripString(31), ForeignKey('IV00101'), primary_key=True)
    location = Column('LOCNCODE', StripString(11), primary_key=True)
    received = Column('DATERECD', DateTime, primary_key=True, default=gp_cur_date)
    dateseq = Column('DTSEQNUM', Integer, primary_key=True, autoincrement=False)
    qtytype = Column('QTYTYPE', Integer, primary_key=True, autoincrement=False, default=1)
    lot = Column('LOTNUMBR', StripString(21), nullable=False)
    cost = Column('UNITCOST', Numeric(19,5), nullable=False)
    qtyreceived = Column('QTYRECVD', Numeric(19,5), nullable=False)
    qtyallocated = Column('ATYALLOC', Numeric(19,5), nullable=False, default=0)
    qtysold = Column('QTYSOLD', Numeric(19,5), nullable=False, default=0)

    def __init__(self, item, location, dateseq, lot, cost, qtyreceived, **kwargs):
        self.item = item
        self.location = location
        self.dateseq = dateseq
        self.lot = lot
        self.cost = cost
        self.qtyreceived = qtyreceived

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass

    def _available(self):
        return self.qtyreceived - (self.qtyallocated >= 0 and self.qtyallocated or 0) - self.qtysold
    available = property(_available)


class IV_Lot_Attribute(Base):
    """ Item Lot Attribute Master """
    __tablename__ = 'IV00301'

    item = Column('ITEMNMBR', StripString(31), primary_key=True)
    lot = Column('LOTNUMBR', StripString(21), primary_key=True)
    attr1 = Column('LOTATRB1', StripString(11), nullable=False, default='')
    attr2 = Column('LOTATRB2', StripString(11), nullable=False, default='')
    attr3 = Column('LOTATRB3', StripString(11), nullable=False, default='')
    attr4 = Column('LOTATRB4', DateTime, nullable=False, default=gp_epoch_start)
    attr5 = Column('LOTATRB5', DateTime, nullable=False, default=gp_epoch_start)

    def __init__(self, item, lot, **kwargs):
        self.item = item
        self.lot = lot

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class IV_UofM_SETP_HDR(Base):
    """ Inventory U of M Schedule Setup """
    __tablename__ = 'IV40201'

    schedule = Column('UOMSCHDL', StripString(11), primary_key=True)
    desc = Column('UMSCHDSC', StripString(31), nullable=False)
    noteidx = Column('NOTEINDX', Numeric(19,5), nullable=False, default=get_next_note_index)
    uom = Column('BASEUOFM', StripString(9), nullable=False)
    dec_places_qtys = Column('UMDPQTYS', Integer, nullable=False, default=1)

    def __init__(self, schedule, desc, uom, **kwargs):
        self.schedule = schedule
        self.desc = desc
        self.uom = uom

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class IV_Location_SETP(Base):
    """ Site Setup """
    __tablename__ = 'IV40700'

    location = Column('LOCNCODE', StripString(11), primary_key=True)
    desc = Column('LOCNDSCR', StripString(31), nullable=False)
    noteidx = Column('NOTEINDX', Numeric(19,5), nullable=False, default=get_next_note_index)

    def __init__(self, location, desc, **kwargs):
        self.location = location
        self.desc = desc

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class IV_TRX_HIST_HDR(Base):
    """ Inventory Transaction History """
    __tablename__ = 'IV30200'
    __table_args__ = (ForeignKeyConstraint(['IVDOCTYP',
                                            'DOCNUMBR',
                                            'SRCRFRNCNMBR',],
                                           ['WO010302.IVDOCTYP',
                                            'WO010302.IVDOCNBR',
                                            'WO010302.MANUFACTUREORDER_I']), {})


    trxsrc = Column('TRXSORCE', StripString(13), primary_key=True)
    doctype = Column('IVDOCTYP', Integer, primary_key=True, autoincrement=False, default=1)
    docnum = Column('DOCNUMBR', StripString(21), primary_key=True)
    docdate = Column('DOCDATE', DateTime, nullable=False)
    batchsrc = Column('BCHSOURC', StripString(15), nullable=False)
    batchnum = Column('BACHNUMB', StripString(15), nullable=False)
    noteidx = Column('NOTEINDX', Numeric(19,5), nullable=False, default=get_next_note_index)
    gl_post_date = Column('GLPOSTDT', DateTime, nullable=False)
    source_ref = Column('SRCRFRNCNMBR', StripString(31), nullable=False)
    source_indicator = Column('SOURCEINDICATOR', Integer, nullable=False)

    def __init__(self, trxsrc, docnum, docdate, batchsrc, batchnum, gl_post_date, source_ref, source_indicator, **kwargs):
        self.trxsrc = trxsrc
        self.docnum = docnum
        self.docdate = docdate
        self.batchsrc = batchsrc
        self.batchnum = batchnum
        self.gl_post_date = gl_post_date
        self.source_ref = source_ref
        self.source_indicator = source_indicator

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass

class IV_TRX_HIST_LINE(Base):
    """ Inventory Transaction Amounts History """
    __tablename__ = 'IV30300'
    __table_args__ = (ForeignKeyConstraint(['TRXSORCE',
                                            'DOCTYPE',
                                            'DOCNUMBR'],
                                           ['IV30200.TRXSORCE',
                                            'IV30200.IVDOCTYP',
                                            'IV30200.DOCNUMBR']),
                      ForeignKeyConstraint(['DOCNUMBR',
                                            'DOCTYPE',
                                            'LNSEQNBR',
                                            'ITEMNMBR'],
                                           ['WO010302.IVDOCNBR',
                                            'WO010302.IVDOCTYP',
                                            'WO010302.LNSEQNBR',
                                            'WO010302.ITEMNMBR']), {})

    trxsrc = Column('TRXSORCE', StripString(13), nullable=False)
    doctype = Column('DOCTYPE', Integer, primary_key=True, autoincrement=False)
    docnum = Column('DOCNUMBR', StripString(21), primary_key=True)
    seq = Column('LNSEQNBR', Numeric(19,5), primary_key=True)
    docdate = Column('DOCDATE', DateTime, nullable=False)
    hist_module = Column('HSTMODUL', StripString(3), nullable=False)
    customer = Column('CUSTNMBR', StripString(15), nullable=False)
    item = Column('ITEMNMBR', StripString(31), nullable=False)
    uom = Column('UOFM', StripString(19), nullable=False)
    trxqty = Column('TRXQTY', Numeric(19,5), nullable=False)
    unitcost = Column('UNITCOST', Numeric(19,5), nullable=False)
    extcost = Column('EXTDCOST', Numeric(19,5), nullable=False)
    trxlocation = Column('TRXLOCTN', StripString(11), nullable=False)
    trx_to_location = Column('TRNSTLOC', StripString(11), nullable=False)
    trx_from_qty_type = Column('TRFQTYTY', Integer, nullable=False, default=1)
    trx_to_qty_type = Column('TRTQTYTY', Integer, nullable=False, default=3)
    invidx = Column('IVIVINDX', Integer, nullable=False)
    invoffset = Column('IVIVOFIX', Integer, nullable=False)
    dec_places_curr = Column('DECPLCUR', Integer, nullable=False, default=3)
    dec_places_qtys = Column('DECPLQTY', Integer, nullable=False, default=1)
    qtybsuom = Column('QTYBSUOM', Numeric(19,5), nullable=False)

    def __init__(self, trxsrc, doctype, docnum, seq, docdate, hist_module, customer, item, uom, trxqty, unitcost, extcost, trxlocation, trx_to_location, invidx, invoffset, qtybsuom, **kwargs):
        self.trxsrc = trxsrc
        self.doctype = doctype
        self.docnum = docnum
        self.seq = seq
        self.docdate = docdate
        self.hist_module = hist_module
        self.customer = customer
        self.item = item
        self.uom = uom
        self.trxqty = trxqty
        self.unitcost = unitcost
        self.extcost = extcost
        self.trxlocation = trxlocation
        self.trx_to_location = trx_to_location
        self.invidx = invidx
        self.invoffset = invoffset
        self.qtybsuom = qtybsuom

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class IV_TRX_HIST_Serial_Lot(Base):
    """ Item Serial and Lot Number History """
    __tablename__ = 'IV30400'
    __table_args__ = (ForeignKeyConstraint(['TRXSORCE',
                                            'IVDOCTYP',
                                            'DOCNUMBR',
                                            'LNSEQNBR',],
                                           ['IV30300.TRXSORCE',
                                            'IV30300.DOCTYPE',
                                            'IV30300.DOCNUMBR',
                                            'IV30300.LNSEQNBR']), {})

    trxsrc = Column('TRXSORCE', StripString(13), primary_key=True)
    doctype = Column('IVDOCTYP', Integer, primary_key=True, autoincrement=False, default=1)
    docnum = Column('DOCNUMBR', StripString(21), primary_key=True)
    seq = Column('LNSEQNBR', Numeric(19,5), primary_key=True)
    lotseq = Column('SLTSQNUM', Integer, primary_key=True, autoincrement=False)
    lot = Column('SERLTNUM', StripString(21), nullable=False)
    qty = Column('SERLTQTY', Numeric(19,5), nullable=False)
    from_bin = Column('FROMBIN', StripString(15), nullable=False)
    to_bin = Column('TOBIN', StripString(15), nullable=False)
    item = Column('ITEMNMBR', StripString(31), nullable=False)
    mfgdate = Column('MFGDATE', DateTime, nullable=False)
    expiration = Column('EXPNDATE', DateTime, nullable=False)

    def __init__(self, trxsrc, docnum, seq, lotseq, lot, qty, from_bin, to_bin, item, mfgdate, expiration, **kwargs):
        self.trxsrc = trxsrc
        self.docnum = docnum
        self.seq = seq
        self.lotseq = lotseq
        self.lot = lot
        self.qty = qty
        self.from_bin = from_bin
        self.to_bin = to_bin
        self.item = item
        self.mfgdate = mfgdate
        self.expiration = expiration

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class IV_TRX_HIST_LINE_DTL(Base):
    """ Inventory Transaction Detail History """
    __tablename__ = 'IV30301'

    doctype = Column('DOCTYPE', Integer, primary_key=True, autoincrement=False)
    docnum = Column('DOCNUMBR', StripString(21), primary_key=True)
    seq = Column('LNSEQNBR', Numeric(19,5), primary_key=True)
    detailseq = Column('DTLSEQNM', Integer, primary_key=True, autoincrement=False)
    qtytype = Column('QTYTYPE', Integer, nullable=False, default=1)
    rctnum = Column('RCPTNMBR', StripString(21), nullable=False)
    qty = Column('RCPTQTY', Numeric(19,5), nullable=False)
    extcost = Column('RCPTEXCT', Numeric(19,5), nullable=False)

    def __init__(self, doctype, docnum, seq, detailseq, rctnum, qty, extcost, **kwargs):
        self.doctype = doctype
        self.docnum = docnum
        self.seq = seq
        self.detailseq = detailseq
        self.rctnum = rctnum
        self.qty = qty
        self.extcost = extcost

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class IV_TRX_HIST_Batch(Base):
    """ Inventory Transaction Batch History """
    __tablename__ = 'IV30100'

    trxsrc = Column('TRXSORCE', StripString(13), primary_key=True)
    batchsrc = Column('BCHSOURC', StripString(15), nullable=False)
    batch = Column('BACHNUMB', StripString(15), nullable=False)
    batch_comment = Column('BCHCOMNT', StripString(61), nullable=False, default='')
    batch_freq = Column('BACHFREQ', Integer, nullable=False, default=1)
    posteddate = Column('POSTEDDT', DateTime, nullable=False)
    hist_removed = Column('HISTRMVD', Integer, nullable=False)
    batch_total = Column('BCHTOTAL', Numeric(19,5), nullable=False)
    control_total = Column('CNTRLTOT', Numeric(19,5), nullable=False)
    control_trx_count = Column('CNTRLTRX', Integer, nullable=False)
    numtrans = Column('NUMOFTRX', Integer, nullable=False)

    def __init__(self, trxsrc, batchsrc, batch, posteddate, hist_removed, batch_total, control_total, control_trx_count, numtrans, **kwargs):
        self.trxsrc = trxsrc
        self.batchsrc = batchsrc
        self.batch = batch
        self.posteddate = posteddate
        self.hist_removed = hist_removed
        self.batch_total = batch_total
        self.control_total = control_total
        self.control_trx_count = control_trx_count
        self.numtrans = numtrans

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass

