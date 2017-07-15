#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import vim  # this is Used for Extending the VimRpc's functionality only
# if you are using this script outside of "vim" it would work perfectly
# without vim support.
import json
from socket import socket, AF_INET, SOCK_STREAM
from rpcbuildenv import master
from __init__ import ModThread

__author__ = 'da-emzy'
__version__ = 1.00
__licenc__ = 'GPLv3'


DATA_V = 8124


class VimRpc():
    """VIMRPC JSON SERVER IMPLEMENTATION"""

    def __init__(self):
        PORT = int(vim.eval('rpc_bind_port'))
        self.PORT = PORT
        self.conn = ''
        self.instance = master
        self.pid = 0
        self.id = 0
        self.num = 3
        self.RESULT = {'Id': self.id,
                       'Result': None,
                       'Error': None}

    def _prepare(self, Ret=None, Err=None):
        """prepare the return value error and id"""
        self.id += 1
        self.RESULT['ID'] = self.id
        self.RESULT['Result'] = Ret
        self.RESULT['Error'] = Err
        return 0

    def _secure(self, method):
        """secure the method being called"""
        method = method
        EVAL = None
        if method.startswith('_'):
            raise AttributeError('ILLEGAL \
                                 PERMISION')
        else:
            EVAL = getattr(self.instance, method)
        return EVAL

    def native_auth(self, conn):
        """reaaaly! a naive auth imp"""
        from os import urandom
        from random import randint
        import hmac
        randbytes = urandom(randint(15, 105))
        KEYID = b'23JKKJNFGJKFGDKDFKFK'
        master_key = hmac.new(KEYID, randbytes).digest()
        HANDSHAKE = conn.recv(len(KEYID))
        client_key = hmac.new(HANDSHAKE, randbytes).digest()
        return hmac.compare_digest(master_key, client_key)

    def deploy(self,):
        connection = socket(AF_INET, SOCK_STREAM)
        PORT = self.PORT
        rpc_bind = vim.eval("g:rpc_bind_address")
        if rpc_bind == 'local':
            r_addr = '127.0.0.1'
        elif rpc_bind == "foreign":
            r_addr = ''
        else:
            raise vim.error("Unknown Option %s \n" % rpc_bind)
        connection.bind((r_addr, PORT))
        connection.listen(3)
        self.conn = connection
        while True:
            host_conn, adr = self.conn.accept()
            self.worker(host_conn, adr)

    def _handler(self, method):
        func = None
        try:
            func = self._secure(method)
        except AttributeError:
            pass
        return func

    def worker(self, _host_b, addr):
        if not self.native_auth(_host_b):
            _host_b.close()
            return 1
        try:
            while True:
                Err = None
                resp = None
                dall = _host_b.recv(DATA_V)
                dall = dall.decode()
                data = json.loads(dall)
                func = data['method']
                arg = data['arg']
                coded = self._handler(func)
                if coded is None:
                    Err = 'UNKNOWN METHOD %s' % func
                else:
                    try:
                        resp = coded(*arg)
                    except Exception as E:
                        Err = str(E)
                self._prepare(Ret=resp, Err=Err)
                sender = json.dumps(self.RESULT)
                sender = sender.encode()
                _host_b.sendall(sender)
        except ValueError:
            pass

    def _fork_serv(self):
        if self.pid == 1:
            print('Json Server Already Running .....')
            return
        num = int(vim.eval('g:rpc_client_conn'))
        self.num = num
        for dae in range(self.num):
            _serv = ModThread(target=self.deploy)
            _serv.daemon = True
            _serv.start()
        self.pid = 1
        print('Starting Json Rpc Server .......')

    def kill_serv(self):
        pid = self.pid
        if pid == 0:
            print('Json Server Not Running ........')
            return
        self.pid = 0
        self.conn.close()
        print('Stopping Json Rpc Server .......')
