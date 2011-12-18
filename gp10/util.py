# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 Sam Widmer <sam@myisteam.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: Sam Widmer <sam@myisteam.com>
# Modified: 2009.05.22 by John Hampton <pacopablo@pacopablo.com>

# Standard Library Imports
from decimal import Decimal
from datetime import datetime

# Third Party Imports
from sqlalchemy.sql import text

# Local Imports
from gp10 import get_session

"""
Utility functions to deal with converting ordinals found in the GP databases.
"""

__all__ = [
    'to_ord',
    'from_ord',
    'gp_cur_date',
    'gp_cur_time',
    'gp_epoch_start',
    'get_next_note_index',
]

def to_ord(num, base=16384):
    """ Convert the decimal number to an integer based ordinal """
    if isinstance(num, basestring):
        num = Decimal(num)
    return int(num * base)

def from_ord(ord, base=16384):
    """ Convert an integer based ordinal to a decimal value

    If the number is a whole number, return an integer.  Otherwise return
    the decimal value
    """
    num = Decimal(ord) / Decimal(base)
    wholenum = int(num)
    return num == wholenum and wholenum or num

def gp_cur_date():
    """ Return the current date w/o the time set """
    return datetime.now().date()

def gp_cur_time():
    """ Return the current time with the date set to the GP epoch start """
    return datetime.combine(gp_epoch_start(), datetime.now().time())

def gp_epoch_start():
    """ Return a date representing the GP epoch: 19000101 00:00:00 """
    return datetime(1900, 1, 1, 0, 0, 0) 

def get_next_note_index(s=None):
    """ Returns the next note index to use.
    
    Calls the `smGetNextNoteIndex` stored procedure to handle the query
    and increment of the company master NOTEINDX

    If a session object is passed, it will use the one specified.  Otherwise
    it will call get_session() to get a session to use.
    """
    txt = """
        SET NOCOUNT ON;
        DECLARE @db AS CHAR(5), @id AS SMALLINT, @noteidx AS NUMERIC(19,5), 
                @err AS INT;
        SELECT @db=CMPANYID 
          FROM DYNAMICS.[dbo].[SY01500]
         WHERE INTERID = DB_Name();
        SELECT @id=@@SPID;
        EXEC DYNAMICS.[dbo].[smGetNextNoteIndex] @db, @id, @noteidx OUTPUT,
                                                 @err OUTPUT;
        SELECT @noteidx, @err;
        SET NOCOUNT OFF;"""[1:]
    s = s and s or get_session()
    r = s.execute(text(txt)).fetchall()
    s.commit()
    return r[0][0]

