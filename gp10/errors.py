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

# Local imports

__all__ = [
    'InsufficientLotQuantity',
    'InvalidSite',
    'InvalidLot',
]

class InsufficientLotQuantity(Exception):
    def __init__(self, lot, qty, available):
        self.lot = lot
        self.qty = qty
        self.available = available

    def __repr__(self):
        return 'InsufficientLotQuantity(%s, %s, %s)' % \
               (str(self.lot), str(self.qty), str(self.available))

    def __str__(self):
        msg = 'InsufficientLotQuantity: %s requested from lot %s, %s ' \
              'are available' % (str(self.qty), str(self.lot), str(self.available))
        return msg


class InvalidSite(Exception):
    def __init__(self, item, site):
        self.item = item
        self.site = site

    def __repr__(self):
        return 'InvalidSite(%s, %s)' % (self.item, self.site)

    def __str__(self):
        msg = 'InvalidSite: %s for item %s ' % (self.site, self.item)
        return msg


class InvalidLot(Exception):
    def __init__(self, item, lot, site):
        self.item = item
        self.lot = lot
        self.site = site

    def __repr__(self):
        return 'InvalidLot(%s, %s, %s)' %  (self.item, self.lot, self.site)

    def __str__(self):
        msg = 'InvalidLot: %s has no lot %s in site %s' % (self.item, self.lot, self.site)
        return msg
