#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def writepid(self):
    """docstring for writepid"""
    curr_pid = os.getpid()
    fhandle = open('/tmp/vimvim.pid', 'a')
    fhandle.write('%s \n' % curr_pid)
    fhandle.close()
