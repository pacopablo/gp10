# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

# Third Party Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

class UnboundMetadataError(Exception):
    pass

def get_session():
    """ Return a session

    The metadata.bind property of the Base class must be set prior to calling
    the function.
    """
    if Base.metadata.bind:
        engine = Base.metadata.bind
    else:
        raise UnboundMetadataError
    sm = sessionmaker(bind=engine)
    return scoped_sesison(sm)

