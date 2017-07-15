#!/usr/bin/env python3
# -*- coding: utf-8 -j-

import vim  # this is Used for Extending the VimRpc's functionality only
# if you are using this script outside of "vim" it would work perfectly
# without vim support.
from xmlrpc.server import SimpleXMLRPCServer
from rpcbuildenv import master
from __init__ import ModThread
__author__ = 'da-emzy'
__version__ = 1.00
__licenc__ = 'GPLv3'


class VimRpc(object):
    """docstring for VIMRPC"""

    def __init__(self):
        PORT = int(vim.eval('rpc_bind_port'))
        rpc_bind = vim.eval("g:rpc_bind_address")
        if rpc_bind == 'local':
            r_addr = '127.0.0.1'
        elif rpc_bind == "foreign":
            r_addr = ''
        else:
            raise vim.error("Unknown Option %s \n" % rpc_bind)
        self.pid = 0
        self.address = r_addr, PORT
        self.mythread = ''
        self.mask = ''

    def deploy(self, num=None):
        addr = self.address
        self.mask = SimpleXMLRPCServer(addr, allow_none=True)
        for cl in master.classes:
            self.mask.register_instance(master)
        return self.mask

    def _fork_serv(self):
        pid = self.pid
        if pid == 1:
            print('Xml Server Already Running ......')
            return
        server = self.deploy()
        num = int(vim.eval('g:rpc_client_conn'))
        for worker in range(num):
            lorris_serv = ModThread(target=server.serve_forever)
            lorris_serv.daemon = True
            lorris_serv.start()
        self.pid = 1
        print('Starting Xml Rpc Server .......')

    def kill_serv(self):
        pid = self.pid
        if pid == 0:
            print('Xml Server Not Running exiting......')
            return
        self.pid = 0
        server = self.mask
        server.server_close()
        print('Stopping Xml Rpc Server .......')
