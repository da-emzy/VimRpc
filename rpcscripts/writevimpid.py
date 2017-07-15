#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def writepid(self):
    """docstring for writepid"""

    curr_pid = os.getpid()
    curr_file = os.environ.get('VIM_PID_F', default='/tmp/hullht.pid')
    fhandle = open(curr_file, 'a')
    fhandle.write('%s \n' % curr_pid)
    fhandle.close()
