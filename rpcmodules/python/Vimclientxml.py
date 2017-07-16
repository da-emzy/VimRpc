#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xmlrpc.client import ServerProxy
import os


__author__ = 'da-emzy'
__version__ = 1.00
__licenc__ = 'GPLv3'


HOST = os.environ.get('VIM_HOST')
PORT = os.environ.get('VIM_PORT')
if HOST is None or PORT is None:
    addr = None
else:
    addr = HOST, PORT


def VimRpc(address=None):
    if address is None:
        address = addr
    if address is None:
        print('ERROR No Valid ADDRESS')
        return -1
    _serv_add = 'http://%s:%s' % (address)
    lorris = ServerProxy(_serv_add, allow_none=True)
    return lorris
