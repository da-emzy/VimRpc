#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from time import sleep
import socket
import json
from collections import namedtuple

__author__ = 'da-emzy'
__version__ = 1.00
__licenc__ = 'GPLv3'

DATA_V = 110124
HOST = os.environ.get('VIM_HOST')
PORT = os.environ.get('VIM_PORT')
if PORT is not None:
    PORT = int(PORT)

Response = namedtuple('Response', 'Result,Error,Id')


class VimRpc(object):
    """docstring for RpcVim"""

    def __init__(self, address=None):
        if address is None:
            address = HOST, PORT
        self.obj = socket.create_connection(address)
        self._native_auth()

    def _native_auth(self):
        HANDSHAKE = os.environ.get('VIM_HANDSHAKE')
        if HANDSHAKE is None:
            HANDSHAKE = '23JKKJNFGJKFGDKDFKFK'
        HANDSHAKE = HANDSHAKE.encode()
        self.obj.send(HANDSHAKE)

    def _json_rpc(self, method, *args):
        data = {'method': method,
                'arg': args}
        request = json.dumps(data)
        self.obj.send(request.encode())
        try:
            response = self.obj.recv(DATA_V)
        except ConnectionResetError:
            self.obj.close()
            print("AUTHENTIFICATION FAILED")
            return
        response = response.decode()
        try:
            decoded = json.loads(response)
        except Exception as e:
            print(str(e).upper())
            sleep(1)
            self.obj.close()
            return 1
        return Response(Result=decoded['Result'],
                        Error=decoded['Error'],
                        Id=decoded['Id'])

    def __getattr__(self, name):
        """docstring for __getattr__"""
        def rpc_init(*arg):
            return self._json_rpc(name, *arg)
        return rpc_init
