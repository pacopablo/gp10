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
from gp10.util import get_next_note_index, gp_cur_date
from gp10.util import gp_cur_time, gp_epoch_start


class MOP_Order_MSTR(Base):
    """ Manufacture Order Master """
    __tablename__ = 'WO010032'

    mo = Column('MANUFACTUREORDER_I', StripString(31), primary_key=True)
    desc = Column('DSCRIPTN', StripString(31), nullable=False, default='')
    status = Column('MANUFACTUREORDERST_I', Integer, nullable=False, default=1)
    fgitem = Column('ITEMNMBR', StripString(31), nullable=False, default='')
    routing = Column('ROUTINGNAME_I', StripString(31), nullable=False, default='')
    endqty = Column('ENDQTY_I', Numeric(19,5), nullable=False, default=1)
    startqty = Column('STARTQTY_I', Numeric(19,5), nullable=False, default=1)
    startdate = Column('STRTDATE', DateTime, nullable=False, default=gp_cur_date)
    starttime = Column('STARTTIME_I', DateTime, nullable=False, default=gp_cur_time)
    enddate = Column('ENDDATE', DateTime, nullable=False, default=gp_cur_time)
    fromsite = Column('DRAWFROMSITE_I', StripString(11), nullable=False, default='PCSF')
    uid = Column('USERID', StripString(15), nullable=False, default='sa')
    schedmethod = Column('SCHEDULEMETHOD_I', Integer, nullable=False, default=1)
    schedpref = Column('SCHEDULINGPREFEREN_I', StripString(21), nullable=False, default='DEFAULT')
    tosite = Column('POSTTOSITE_I', StripString(11), nullable=False, default='PCSF')
    priority = Column('MANUFACTUREORDPRI_I', Integer, nullable=False, default=2)
    outsourced = Column('OUTSOURCED_I', Integer, nullable=False, default=1)
    bomcat = Column('BOMCAT_I', Integer, nullable=False, default=1)
    noteidx = Column('NOTEINDX', Numeric(19,5), nullable=False, default=get_next_note_index)


    def __init__(self, mo, **kwargs):
        self.mo = mo

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_Item_MSTR(Base):
    """ Picklist File """
    __tablename__ = 'PK010033'

    mo = Column('MANUFACTUREORDER_I', StripString(31), ForeignKey('WO010032.MANUFACTUREORDER_I'), primary_key=True)
    seq = Column('SEQ_I', Integer, primary_key=True, autoincrement=False)
    fgitem = Column('PPN_I', StripString(31), primary_key=True, default='')
    item = Column('ITEMNMBR', StripString(31), ForeignKey('IV00101.ITEMNMBR'), primary_key=True)
    status = Column('MANUFACTUREORDERST_I', Integer, nullable=False, default=1)
    posnum = Column('POSITION_NUMBER', Integer, nullable=False, default=0)
    routing = Column('ROUTINGNAME_I', StripString(31), nullable=False)
    mrpamt = Column('MRPAMOUNT_I', Numeric(19,5), nullable=False)
    reqqty = Column('SUGGESTEDQTY_I', Numeric(19,5), nullable=False)
    qtyissued = Column('QTY_ISSUED_I', Numeric(19,5), nullable=False, default=Decimal(0))
    qtyallocated = Column('ATYALLOC', Numeric(19,5), nullable=False, default=Decimal(0))
    wc = Column('WCID_I', StripString(11), nullable=False)
    routeseq = Column('RTSEQNUM_I', StripString(11), nullable=False)
    location = Column('LOCNCODE', StripString(11), nullable=False, default='PCSF')
    changedate = Column('CHANGEDATE_I', DateTime, nullable=False, default=gp_cur_date)
    uid = Column('USERID', StripString(15), nullable=False, default='sa')
    qtyallowed = Column('QTY_ALLOWED_I', Numeric(19,5), nullable=False)
    reqdate = Column('REQDATE', DateTime, nullable=False, default=gp_cur_date)
    uom = Column('UOFM', StripString(9), nullable=False, default='Each')
    qtybsuom = Column('QTYBSUOM', Numeric(19,5), nullable=False, default=1)
    bomseq = Column('BOMSEQ_I', Integer, nullable=False)
    bomcat = Column('BOMCAT_I', Integer, nullable=False, default=1)
    posnum2 = Column('POSITION_NUMBER2', Integer, nullable=False)
    isallocated = Column('ALLOCATED_I', Integer, nullable=False, default=0)
    allocateuid = Column('ALLOCATEUID_I', StripString(15), nullable=False, default='sa')
    allocatedate = Column('ALLOCATEDATEI', DateTime, nullable=False, default=gp_cur_date)
    allocatetime = Column('ALLOCATETIMEI', DateTime, nullable=False, default=gp_cur_time)

    def __init__(self, mo, seq, item, routing, reqqty, wc, routeseq, **kwargs):
        self.mo = mo
        self.seq = seq
        self.item = item
        self.routing = routing
        self.mrpamt = self.reqqty
        self.reqqty = reqqty
        self.wc = wc
        self.routeseq = routeseq
        self.qtyallowed = self.reqqty
        self.bomseq = self.seq
        self.posnum2 = self.seq

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class IV_Item_ENG(Base):
    """ Item Engineering File """
    __tablename__ = 'IVR10015'

    item = Column('ITEMNMBT', StripString(32), primary_key=True)
    status = Column('ITEMSTATUS_I', Integer, nullable=False, default=1)
    makebuycode = Column('MAKEBUYCODE_I', Integer, nullable=False, default=1)
    effective_date = Column('EFFECTIVEDATE_I', DateTime, nullable=False)

    def __init__(self, item, **kwargs):
        self.item = item
        self.effective_date = datetime.now().date()

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class WC_HDR(Base):
    """ Work Center Header File """
    __tablename__ = 'WC010931'

    wc = Column('WCID_I', StripString(11), ForeignKey('WC010015.WCID_I'), primary_key=True)
    desc = Column('WCDESC_I', StripString(31), nullable=False)
    outsourced = Column('OUTSOURCED_I', Integer, nullable=False, default=1)

    def __init__(self, wc, **kwargs):
        self.wc = wc
        self.desc = wc

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_Routing_Line(Base):
    """  """
    __tablename__ = 'WR010130'

    mo = Column('MANUFACTUREORDER_I', StripString(31), ForeignKey('WO010032.MANUFACTUREORDER_I'), primary_key=True)
    routeseq = Column('RTSEQNUM_I', StripString(11), primary_key=True)
    seqtype = Column('RTSEQTYPE_I', Integer, nullable=False, default=1)
    startdate = Column('SCHEDULESTARTDATE_I', DateTime, nullable=False, default=gp_cur_date)
    finishdate = Column('SCHEDULEFINISHDATE_I', DateTime, nullable=False, default=gp_cur_date)
    wc = Column('WCID_I', StripString(11), nullable=False)
    desc = Column('RTSEQDES_I', StripString(11), nullable=False)
    uid = Column('USERID', StripString(15), nullable=False, default='sa')
    createddate = Column('CREATDDT', DateTime, nullable=False, default=gp_cur_date)
    createdtime = Column('CREATETIME_I', DateTime, nullable=False, default=gp_cur_time)
    mostartqty = Column('WIPOPPERMOSTARTQTY', Integer, nullable=False, default=1)
    noteidx = Column('NOTEINDX', Numeric(19,5), nullable=False, default=get_next_note_index)

    def __init__(self, mo, routeseq, wc, **kwargs):
        self.mo = mo
        self.routeseq = routeseq
        self.wc = wc
        self.desc = self.wc

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_Order_Activity(Base):
    """ Manufacture Order Activity """
    __tablename__ = 'MOP10213'

    mo = Column('MANUFACTUREORDER_I', StripString(31), ForeignKey('WO010032.MANUFACTUREORDER_I'), primary_key=True)
    linenum = Column('LNSEQNBR', Numeric(19,5), primary_key=True, default=1)
    status = Column('MANUFACTUREORDERST_I', Integer, nullable=False, default=1)
    activity = Column('MO_ACTIVITY_REASON_I', Integer, nullable=False, default=47)
    changeddate = Column('CHANGEDATE_I', DateTime, nullable=False, default=gp_cur_date)
    changedtime = Column('TIME_I', DateTime, nullable=False, default=gp_cur_time)
    uid = Column('USERID', StripString(15), nullable=False, default='sa')
    picknum = Column('PICKNUMBER', StripString(17), nullable=False, default='')
    doctype = Column('DOCTYPE', Integer, nullable=False, default=0)

    def __init__(self, mo, **kwargs):
        self.mo = mo

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_Picklist_Seq_MSTR(Base):
    """ Picklist Sequence Master """
    __tablename__ = 'PK01200'

    mo = Column('MANUFACTUREORDER_I', StripString(31), ForeignKey('WO010032.MANUFACTUREORDER_I'), primary_key=True)
    pciklistseq = Column('PICKLISTSEQ', Integer, nullable=False, default=1)

    def __init__(self, mo, **kwargs):
        self.mo = mo

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class WC_MSTR(Base):
    """ Work Center Master File """
    __tablename__ = 'WC010015'

    wc = Column('WCID_I', StripString(11), primary_key=True)
    effective_date = Column('EFFECTIVEDATE_I', DateTime, primary_key=True, default=gp_cur_date)
    noteidx = Column('NOTEINDX', Numeric(19,5), nullable=False, default=get_next_note_index)

    def __init__(self, wc, **kwargs):
        self.wc = wc

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_PickDoc_Line(Base):
    """  """
    __tablename__ = 'MOP1210'

    picknum = Column('PICKNUMBER', StripString(17), primary_key=True)
    linenum = Column('PICKDOCLINENUM', Integer, primary_key=True, autoincrement=False)
    mo = Column('MANUFACTUREORDER_I', StripString(31), nullable=False)
    posnum = Column('POSITION_NUMBER', Integer, nullable=False)
    item = Column('ITEMNMBR', StripString(31), nullable=False)
    picklistseq = Column('PICKLISTSEQ', Integer, nullable=False)
    pickqty = Column('TRXQTY', Numeric(19,5), nullable=False)
    uom = Column('UOFM', StripString(9), nullable=False)
    tosite = Column('TO_SITE_I', StripString(11), nullable=False)
    location = Column('FROM_SITE_I', StripString(11), nullable=False, default='PCSF')
    uomqty = Column('QTYBSUOM', Numeric(19,5), nullable=False, default=1)
    item_tracking = Column('ITMTRKOP', Integer, nullable=False, default=3)
    qtyallocated = Column('ATYALLOC', Numeric(19,5), nullable=False)
    qtyselected = Column('QTYSLCTD', Numeric(19,5), nullable=False)
    qtyissued = Column('QTY_ISSUED_I', Numeric(19,5), nullable=False)
    mrpamt = Column('MRPAMOUNT_I', Numeric(19,5), nullable=False)
    reqdate = Column('REQDATE', DateTime, nullable=False, default=gp_cur_date)
    pickdate = Column('DATEPICKED', DateTime, nullable=False, default=gp_cur_date)
    trxtype = Column('TRX_TYPE', Integer, nullable=False, default=1)

    def __init__(self, picknum, linenum, mo, posnum, item, picklistseq, pickqty, uom, tosite, qtyallocated, **kwargs):
        self.picknum = picknum
        self.linenum = linenum
        self.mo = mo
        self.posnum = posnum
        self.item = item
        self.picklistseq = picklistseq
        self.pickqty = pickqty
        self.uom = uom
        self.tosite = tosite
        self.qtyallocated = qtyallocated
        self.qtyselected = self.qtyallocated
        self.qtyissued = self.qtyallocated
        self.mrpamt = self.qtyallocated

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_PickDoc_MSTR(Base):
    """  """
    __tablename__ = 'MOP1200'

    picknum = Column('PICKNUMBER', StripString(17), primary_key=True)
    trxtype = Column('TRX_TYPE', Integer, nullable=False, default=1)
    uid = Column('USERID', StripString(15), nullable=False, default='sa')
    changedate = Column('CHANGEDATE_I', DateTime, nullable=False, default=gp_cur_time)
    docdate = Column('DOCDATE', DateTime, nullable=False, default=gp_cur_time)
    posteddate = Column('POSTEDDT', DateTime, nullable=False, default=gp_cur_date)
    posted = Column('POSTED', Boolean, nullable=False, default=False)

    def __init__(self, picknum, **kwargs):
        self.picknum = picknum

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_Pending_Serial_Lot(Base):
    """ Manufacture Order Lot Issue """
    __tablename__ = 'MOP1020'
    __table_args__ = (ForeignKeyConstraint(['MANUFACTUREORDER_I',
                                            'PICKLISTSEQ',
                                            'ITEMNMBR'],
                                           ['PK010033.MANUFACTUREORDER_I',
                                            'PK010033.SEQ_I',
                                            'PK010033.ITEMNMBR']),
                      ForeignKeyConstraint(['MANUFACTUREORDER_I',
                                            'DOCNUMBR',
                                            'PICKLISTSEQ',
                                            'PICKDOCLINENUM',
                                            'ITEMNMBR'],
                                           ['MOP1210.MANUFACTUREORDER_I',
                                            'MOP1210.PICKNUMBER',
                                            'MOP1210.PICKLISTSEQ',
                                            'MOP1210.PICKDOCLINENUM',
                                            'MOP1210.ITEMNMBR']), {})

    mo = Column('MANUFACTUREORDER_I', StripString(31), primary_key=True)
    docnum = Column('DOCNUMBR', StripString(21), primary_key=True)
    pickseq = Column('PICKLISTSEQ', Integer, primary_key=True, autoincrement=False)
    calledby = Column('CALLEDBY', Integer, primary_key=True, autoincrement=False, default=1)
    pickdoclinenum = Column('PICKDOCLINENUM', Integer, primary_key=True, autoincrement=False)
    seq = Column('SEQ_I', Integer, primary_key=True, autoincrement=False)
    location = Column('FROM_SITE_I', StripString(11), primary_key=True, default='PCSF')
    trxtype = Column('TRX_TYPE', Integer, primary_key=True, autoincrement=False, default=1)
    item = Column('ITEMNMBR', StripString(31), nullable=False)
    lot = Column('SERLTNUM', StripString(21), nullable=False)
    qty = Column('SERLTQTY', Numeric(19,5), nullable=False)
    tosite = Column('TO_SITE_I', StripString(11), nullable=False)
    recvdate = Column('DATERECD', DateTime, nullable=False)
    dateseq = Column('DTSEQNUM', Numeric(19,5), nullable=False)
    linenum = Column('LineNumber', Integer, nullable=False)
    item_tracking = Column('ITMTRKOP', Integer, nullable=False, default=3)

    def __init__(self, mo, docnum, pickseq, pickdoclinenum, seq, item, lot, qty, tosite, recvdate, dateseq, linenum, **kwargs):
        self.mo = mo
        self.docnum = docnum
        self.pickseq = pickseq
        self.pickdoclinenum = pickdoclinenum
        self.seq = seq
        self.item = item
        self.lot = lot
        self.qty = qty
        self.tosite = tosite
        self.recvdate = recvdate
        self.dateseq = dateseq
        self.linenum = linenum

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_Pending_Serial_Lot_HIST(Base):
    """ Manufacture Order Lot Issue HIST """
    __tablename__ = 'MOP1090'
    __table_args__ = (ForeignKeyConstraint(['MANUFACTUREORDER_I',
                                            'PICKLISTSEQ',
                                            'ITEMNMBR'],
                                           ['PK010033.MANUFACTUREORDER_I',
                                            'PK010033.SEQ_I',
                                            'PK010033.ITEMNMBR']),
                      ForeignKeyConstraint(['MANUFACTUREORDER_I',
                                            'DOCNUMBR',
                                            'PICKLISTSEQ',
                                            'PICKDOCLINENUM',
                                            'ITEMNMBR'],
                                           ['MOP1210.MANUFACTUREORDER_I',
                                            'MOP1210.PICKNUMBER',
                                            'MOP1210.PICKLISTSEQ',
                                            'MOP1210.PICKDOCLINENUM',
                                            'MOP1210.ITEMNMBR']), {})

    mo = Column('MANUFACTUREORDER_I', StripString(31), primary_key=True)
    docnum = Column('DOCNUMBR', StripString(21), primary_key=True)
    pickseq = Column('PICKLISTSEQ', Integer, primary_key=True, autoincrement=False)
    calledby = Column('CALLEDBY', Integer, primary_key=True, autoincrement=False, default=1)
    pickdoclinenum = Column('PICKDOCLINENUM', Integer, primary_key=True, autoincrement=False)
    seq = Column('SEQ_I', Integer, primary_key=True, autoincrement=False)
    location = Column('FROM_SITE_I', StripString(11), primary_key=True, default='PCSF')
    trxtype = Column('TRX_TYPE', Integer, primary_key=True, autoincrement=False, default=1)
    item = Column('ITEMNMBR', StripString(31), nullable=False)
    lot = Column('SERLTNUM', StripString(21), nullable=False)
    qty = Column('SERLTQTY', Numeric(19,5), nullable=False)
    tosite = Column('TO_SITE_I', StripString(11), nullable=False)
    recvdate = Column('DATERECD', DateTime, nullable=False)
    dateseq = Column('DTSEQNUM', Numeric(19,5), nullable=False)
    linenum = Column('LineNumber', Integer, nullable=False)
    item_tracking = Column('ITMTRKOP', Integer, nullable=False, default=3)

    def __init__(self, mo, docnum, pickseq, pickdoclinenum, seq, item, lot, qty, tosite, recvdate, dateseq, linenum, **kwargs):
        self.mo = mo
        self.docnum = docnum
        self.pickseq = pickseq
        self.pickdoclinenum = pickdoclinenum
        self.seq = seq
        self.item = item
        self.lot = lot
        self.qty = qty
        self.tosite = tosite
        self.recvdate = recvdate
        self.dateseq = dateseq
        self.linenum = linenum

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class routing_mstr(Base):
    """  """
    __tablename__ = 'RT010001'

    item = Column('ITEMNMBR', StripString(31), primary_key=True)
    name = Column('ROUTINGNAME_I', StripString(31), primary_key=True)
    routeprimary = Column('RTPRIMARY_I', Integer, nullable=False, default=1)
    routestatus = Column('RTSTATUSDDL_I', Integer, nullable=False, default=4)
    noteidx = Column('NOTeINDX', Numeric(19,5), nullable=False, default=get_next_note_index)

    def __init__(self, item, name, **kwargs):
        self.item = item
        self.name = name

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class routing_line(Base):
    """  """
    __tablename__ = 'RT010130'
    __table_args__ = (ForeignKeyConstraint(['ROUTINGNAME_I',
                                            'ITEMNMBR'],
                                           ['RT010001.ROUTINGNAME_I',
                                            'RT010001.ITEMNMBR']), {})

    name = Column('ROUTINGNAME_I', StripString(31), primary_key=True)
    item = Column('ITEMNMBR', StripString(31), primary_key=True)
    routeseq = Column('RTSEQNUM_I', StripString(11), primary_key=True)
    routedesc = Column('RTSEQDES_I', StripString(101), nullable=False)
    wcid = Column('WCID_I', StripString(11), nullable=False)
    noteidx = Column('NOTEINDX', Numeric(19,5), nullable=False, default=get_next_note_index)

    def __init__(self, name, item, routeseq, routedesc, wcid, **kwargs):
        self.name = name
        self.item = item
        self.routeseq = routeseq
        self.routedesc = routedesc
        self.wcid = wcid

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class BOM_Revision(Base):
    """  """
    __tablename__ = 'BM010415'

    item = Column('ITEMNMBR', StripString(31), primary_key=True)
    cat = Column('BOMCAT_I', Integer, primary_key=True, autoincrement=False, default=1)
    name = Column('BOMNAME_I', StripString(15), primary_key=True, default='')
    revlevel = Column('REVISIONLEVEL_I', StripString(51), nullable=False, default='1')
    backflush = Column('BACKFLUSHITEM_I', Integer, nullable=False, default=0)
    type = Column('BOMTYPE_I', Integer, nullable=False, default=1)
    phantominventory = Column('Net_Phanton_Inventory', Integer, nullable=False, default=0)
    changed = Column('CHANGEDATE_I', DateTime, nullable=False)
    changedby = Column('CHANGEBY_I', StripString(15), nullable=False, default='sa')
    noteidx = Column('MFGNOTEINDEX3_I', Numeric(19,5), nullable=False, default=Decimal(0))

    def __init__(self, item, changed, **kwargs):
        self.item = item
        self.changed = changed

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_Picklist_Site_QTYS(Base):
    """  """
    __tablename__ = 'MOP1400'
    __table_args__ = (ForeignKeyConstraint(['MANUFACTUREORDER_I',
                                            'PICKLISTSEQ',
                                            'LOCNCODE'],
                                           ['PK010033.MANUFACTUREORDER_I',
                                            'PK010033.SEQ_I',
                                            'PK010033.LOCNCODE']), {})

    mo = Column('MANUFACTUREORDER_I', StripString(31), primary_key=True)
    seq = Column('PICKLISTSEQ', Integer, primary_key=True, autoincrement=False)
    location = Column('LOCNCODE', StripString(11), primary_key=True)
    item = Column('ITEMNMBR', StripString(31), nullable=False)
    qtyissued = Column('QTY_ISSUED_I', Numeric(19,5), nullable=False, default=0)
    qtyallocated = Column('ATYALLOC', Numeric(19,5), nullable=False, default=0)
    numscrapped = Column('NUMBERSCRAPPED_I', Numeric(19,5), nullable=False, default=0.0)
    issuependingqty = Column('PENDING_ISSUE_QTY_I', Numeric(19,5), nullable=False, default=0.0)
    revissuependingqty = Column('PENDING_REV_ISS_QTY_I', Numeric(19,5), nullable=False, default=0.0)
    scrappendingqty = Column('PENDING_SCRAP_QTY_I', Numeric(19,5), nullable=False, default=0.0)
    revscrappendingqty = Column('PENDING_REV_SCRAP_QTY_I', Numeric(19,5), nullable=False, default=0.0)

    def __init__(self, mo, seq, location, item, **kwargs):
        self.mo = mo
        self.seq = seq
        self.location = location
        self.item = item

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_WIP_Stack(Base):
    """ MOP WIP Stack """
    __tablename__ = 'MOP1000'

    mo = Column('MANUFACTUREORDER_I', StripString(31), primary_key=True)
    item = Column('ITEMNMBR', StripString(31), primary_key=True)
    tosite = Column('TO_SITE_I', StripString(11), primary_key=True)
    recvdate = Column('DATERECD', DateTime, primary_key=True)
    wipseq = Column('WIPSEQNMBR', Numeric(19,5), primary_key=True)
    picklistseq = Column('PICKLISTSEQ', Integer, nullable=False)
    picknum = Column('PICKNUMBER', StripString(17), nullable=False)
    pickdoclinenum = Column('PICKDOCLINENUM', Integer, nullable=False)
    wipqty = Column('WIPQTYSOLD', Integer, nullable=False)
    qtyreceived = Column('QTYRECVD', Numeric(19,5), nullable=False)
    qtysold = Column('QTYSOLD', Numeric(19,5), nullable=False)
    invdocnum = Column('IVDOCNBR', StripString(17), nullable=False)
    receiptseq = Column('RCTSEQNM', Integer, nullable=False)
    item_tracking = Column('ITMTRKOP', Integer, nullable=False)
    item_cost_array_1 = Column('ITEM_COSTS_ARRAY_I_1', Numeric(19,5), nullable=False)
    item_cost_array_10 = Column('ITEM_COSTS_ARRAY_I_10', Numeric(91,5), nullable=False)
    routeseq = Column('RTSEQNUM_I', StripString(11), nullable=False)
    fromsite = Column('FROM_SITE_I', StripString(11), nullable=False)
    date_received_in_inventory = Column('DTRCVDINVNTRY', DateTime, nullable=False)
    backflsuh = Column('BACKFLUSHITEM_I', Integer, nullable=False)
    numscrapped = Column('NUMBERSCRAPPED_I', Numeric(19,5), nullable=False)

    def __init__(self, mo, item, tosite, recvdate, wipseq, picklistseq, picknum, pickdoclinenum, wipqty, qtyreceived, qtysold, invdocnum, receiptseq, item_tracking, item_cost_array_1, item_cost_array_10, routeseq, fromsite, date_received_in_inventory, backflsuh, numscrapped, **kwargs):
        self.mo = mo
        self.item = item
        self.tosite = tosite
        self.recvdate = recvdate
        self.wipseq = wipseq
        self.picklistseq = picklistseq
        self.picknum = picknum
        self.pickdoclinenum = pickdoclinenum
        self.wipqty = wipqty
        self.qtyreceived = qtyreceived
        self.qtysold = qtysold
        self.invdocnum = invdocnum
        self.receiptseq = receiptseq
        self.item_tracking = item_tracking
        self.item_cost_array_1 = item_cost_array_1
        self.item_cost_array_10 = item_cost_array_10
        self.routeseq = routeseq
        self.fromsite = fromsite
        self.date_received_in_inventory = date_received_in_inventory
        self.backflsuh = backflsuh
        self.numscrapped = numscrapped

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class MOP_Lot_Issue(Base):
    """ Manufacture Order Lot Issue """
    __tablename__ = 'WO010302'

    mo = Column('MANUFACTUREORDER_I', StripString(31), primary_key=True)
    lot = Column('LOTNUMBR', StripString(21), primary_key=True)
    lineseq = Column('LNSEQNBR', Numeric(19,5), primary_key=True)
    linenum = Column('LineNumber', Integer, primary_key=True, autoincrement=False)
    item = Column('ITEMNMBR', StripString(31), nullable=False)
    qty = Column('SERLTQTY', Numeric(19,5), nullable=False)
    seriallotseq = Column('SLTSQNUM', Integer, nullable=False)
    location = Column('LOCNCODE', StripString(11), nullable=False)
    wc = Column('WCID_I', StripString(11), nullable=False)
    receiveddate = Column('DATERECD', DateTime, nullable=False)
    dateseq = Column('DTSEQNUM', Numeric(19,5), nullable=False)
    posted = Column('POSTED', Integer, nullable=False)
    invdocnum = Column('IVDOCNBR', StripString(17), nullable=False)
    invdoctype = Column('IVDOCTYP', Integer, nullable=False)
    wipseq = Column('WIPSEQNMBR', Numeric(19,5), nullable=False)
    qtyconsumed = Column('QTYCONSUMED', Numeric(19,5), nullable=False)
    qtypending = Column('QTYPENDING', Numeric(19,5), nullable=False)
    qtyallocated = Column('ATYALLOC', Numeric(19,5), nullable=False)
    picknum = Column('PICKNUMBER', StripString(17), nullable=False)
    picklistseq = Column('PICKLISTSEQ', Integer, nullable=False)
    rowid = Column('ROWID', Integer, nullable=False)
    expirationdate = Column('EXPNDATE', DateTime, nullable=False)
    manufacturedate = Column('MFGDATE', DateTime, nullable=False)

    def __init__(self, mo, lot, lineseq, linenum, item, qty, seriallotseq, location, wc, receiveddate, dateseq, posted, invdocnum, invdoctype, wipseq, qtyconsumed, qtypending, qtyallocated, picknum, picklistseq, rowid, expirationdate, manufacturedate, **kwargs):
        self.mo = mo
        self.lot = lot
        self.lineseq = lineseq
        self.linenum = linenum
        self.item = item
        self.qty = qty
        self.seriallotseq = seriallotseq
        self.location = location
        self.wc = wc
        self.receiveddate = receiveddate
        self.dateseq = dateseq
        self.posted = posted
        self.invdocnum = invdocnum
        self.invdoctype = invdoctype
        self.wipseq = wipseq
        self.qtyconsumed = qtyconsumed
        self.qtypending = qtypending
        self.qtyallocated = qtyallocated
        self.picknum = picknum
        self.picklistseq = picklistseq
        self.rowid = rowid
        self.expirationdate = expirationdate
        self.manufacturedate = manufacturedate

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass

