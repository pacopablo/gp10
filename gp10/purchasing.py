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
from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relation
from sqlalchemy.ext.associationproxy import association_proxy

# Local imports
from gp10 import Base, get_session
from gp10.types import StripString, Ordinal
from gp10.util import get_session, get_next_note_index, gp_cur_date
from gp10.util import gp_cur_time, gp_epoch_start

class PM_Vendor_MSTR(Base):
    """ PM Vendor Master File """
    __tablename__ = 'PM00200'

    vendid = Column('VENDORID', StripString(15), primary_key=True)
    shipmethod = Column('SHIPMTHD', StripString(15), nullable=False)

    def __init__(self, vendid, shipmethod, **kwargs):
        self.vendid = vendid
        self.shipmethod = shipmethod

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class POP_ReceiptHist(Base):
    """ Purchasing Receipt History """
    __tablename__ = 'POP30300'

    rctnum = Column('POPRCTNM', StripString(17), primary_key=True)
    receiptdate = Column('receiptdate', DateTime, nullable=False)
    batchnum = Column('BACHNUMB', StripString(15), nullable=False)
    vendid = Column('VENDORID', StripString(15), nullable=False)
    vendname = Column('VENDNAME', StripString(65), nullable=False)
    venddocnum = Column('VNDDOCNM', StripString(21), nullable=False)
    created = Column('CREATDDT', DateTime, nullable=False, default=gp_cur_date)
    modified = Column('MODIFDT', DateTime, nullable=False, default=gp_cur_date)
    currency = Column('CURNCYID', StripString(15), nullable=False, default=get_currency)
    shipmethod = Column('SHIPMTHD', StripString(15), nullable=False)

    def __init__(self, rctnum, receiptdate, batchnum, vendid, vendname, venddocnum, **kwargs):
        self.rctnum = rctnum
        self.receiptdate = receiptdate
        self.batchnum = batchnum
        self.vendid = vendid
        self.vendname = vendname
        self.venddocnum = venddocnum
        self.shipmethod = get_vendor_ship_method(self.vendid)

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass


class POP_Receipt(Base):
    """ Purchasing Receipt Work """
    __tablename__ = 'POP10300'

    rctnum = Column('POPRCTNM', StripString(17), primary_key=True)
    receiptdate = Column('receiptdate', DateTime, nullable=False, default=gp_cur_date)
    glpostdate = Column('GLPOSTDT', DateTime, nullable=False, default=gp_cur_date)
    batchnum = Column('BACHNUMB', StripString(15), nullable=False)
    vendid = Column('VENDORID', StripString(15), nullable=False)
    vendname = Column('VENDNAME', StripString(65), nullable=False)
    venddocnum = Column('VNDDOCNM', StripString(21), nullable=False)
    created = Column('CREATDT', DateTime, nullable=False, default=gp_cur_date)
    modified = Column('MODIFDT', DateTime, nullable=False, default=gp_cur_date)
    currency = Column('CURNCYID', StripString(15), nullable=False, default=get_currency)
    shipmethod = Column('SHIPMTHD', StripString(15), nullable=False)
    subtotal = Column('SUBTOTAL', Numeric(19,5), nullable=False, default=Decimal(0))
    orig_subtotal = Column('ORDUBTOT', Numeric(19,5), nullable=False, default=Decimal(0))
    purchasetype = Column('POPTYPE', Integer, nullable=False, default=1)
    batchsrc = Column('BCHSOURC', StripString(15), nullable=False, default='Rcvg Trx Entry')
    terms = Column('PYMTRMID', StripString(21), nullable=False, default='Net 30')
    duedate = Column('DUEDATE', DateTime, nullable=False)
    reference = Column('REFERENCE', StripString(31), nullable=False, default='Receivings Transaction Entry')
    uid = Column('USER2ENT', StripString(15), nullable=False, default='sa')
    currencyindex = Column('CURRNIDX', Integer, nullable=False)
    freight_taxable = Column('Purchase_Freight_Taxable', Integer, nullable=False, default=2)
    misc_taxable = Column('Purchase_Misc_Taxable', Integer, nullable=False, default=2)
    addrcode = Column('VADCDTRO', StripString(15), nullable=False, default='REMIT TO')
    landedcost = Column('Total_Landed_Cost_Amount', Numeric(19,5), nullable=False, default=Decimal(0))

    def __init__(self, rctnum, batchnum, vendid, vendname, venddocnum, **kwargs):
        self.rctnum = rctnum
        self.batchnum = batchnum
        self.vendid = vendid
        self.vendname = vendname
        self.venddocnum = venddocnum
        self.shipmethod = get_vendor_ship_method(self.vendid)
        self.duedate = datetime(2017, 5, 12).date()
        self.currencyindex = get_currency_idx(self.currency)

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass

class POP_ReceiptLine(Base):
    """ Purchasing Receipt Line """
    __tablename__ = 'POP10310'

    rctnum = Column('POPRCTNM', StripString(17), primary_key=True)
    line = Column('RCPTLNNM', Integer, primary_key=True, autoincrement=False)
    po = Column('PONUMBER', StripString(17), nullable=False)
    item = Column('ITEMNMBR', StripString(31), nullable=False)
    itemdesc = Column('ITEMSDESC', StripString(101), nullable=False)
    venditem = Column('VNDITNUM', StripString(31), nullable=False)
    venddesc = Column('VNDITDSC', StripString(101), nullable=False)
    qty_in_base_uom = Column('UMQTYINB', Numeric(19,5), nullable=False)
    invindx = Column('INVINDX', Integer, nullable=False)
    uom = Column('UOFM', StripString(9), nullable=False)
    unitcost = Column('UNITCOST', Numeric(19,5), nullable=False)
    extcost = Column('EXTDCOST', Numeric(19,5), nullable=False, default=Decimal(0))
    location = Column('LOCNCODE', StripString(11), nullable=False)
    dec_places_curr = Column('DECPLCUR', Integer, nullable=False, default=3)
    dec_places_qtys = Column('DECPLQTY', Integer, nullable=False, default=3)
    itemtracking = Column('ITMTRKOP', Integer, nullable=False, default=3)
    valmethod = Column('VCNTMTHD', Integer, nullable=False, default=1)
    currency = Column('CURNCYID', StripString(15), nullable=False)
    orig_unitcost = Column('ORUNTCST', Numeric(19,5), nullable=False)
    currency_idx = Column('CURRNIDX', Integer, nullable=False)
    orig_extcost = Column('OREXTCST', Numeric(19,5), nullable=False, default=Decimal(0))
    orig_dec_places_cur = Column('ODECPLCU', Integer, nullable=False, default=2)
    purchase_inv_item_taxable = Column('Purchase_IV_Item_Taxable', Integer, nullable=False, default=2)
    reval_inventory = Column('Revalue_Inventory', Integer, nullable=False, default=1)
    purchase_price_variance_idx = Column('PURPVIDX', Integer, nullable=False)
    remaining_ap_amt = Column('Remaining_AP_Amount', Numeric(19,5), nullable=False, default=Decimal(0))
    shipmethod = Column('SHIPMTHD', StripString(15), nullable=False)

    def __init__(self, rctnum, line, po, item, itemdesc, venditem, venddesc,
                 qty_in_base_uom, invindx, uom, unitcost, location, currency,
                 orig_unitcost, currency_idx, purchase_price_variance_idx,
                 shipmethod, **kwargs):
        self.rctnum = rctnum
        self.line = line
        self.po = po
        self.item = item
        self.itemdesc = itemdesc
        self.venditem = venditem
        self.venddesc = venddesc
        self.qty_in_base_uom = qty_in_base_uom
        self.invindx = invindx
        self.uom = uom
        self.unitcost = unitcost
        self.location = location
        self.currency = currency
        self.orig_unitcost = orig_unitcost
        self.currency_idx = currency_idx
        self.purchase_price_variance_idx = purchase_price_variance_idx
        self.shipmethod = shipmethod

        for k, v in kwargs.items():
            setattr(self, k, v)

        pass

