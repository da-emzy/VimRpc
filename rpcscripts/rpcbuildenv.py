#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import os
# import sys
import os
import vim  # +py[2-3] support
from os import path

__author__ = 'da-emzy'
__version__ = 1.00
__licenc__ = 'GPLv3'


class VimObject(object):
    """A OBJECT TO SIMPLIFY VIM Functions
    For use with "VIMRPCENV"
    """

    def __init__(self):
        """ INITIALIAZE Class Variables"""
        self.tabs = vim.tabpages
        self.window = vim.windows
        self.buffer = vim.buffers
        self.vim = vim

    def cursor(self):
        # return current cursor positiom
        return_value = vim.current.window.cursor
        return return_value

    def move(self, line, col, win=vim.current.window):
        # move to a positiom win / the current window
        # if win is not specified
        vim.current.window = win
        pos = win.cursor
        win.cursor = (line, col)
        return pos

    def curbuf(self):
        # return vim current buffer object
        return vim.current.buffer

    def curwin(self):
        # return vim current window object
        return vim.current.window

    def eval(self, data):
        # evaluate a vim expr and return the evaluated
        # string
        value = vim.eval(data)
        return value

    def do(self, argus):
        # run an extern vim command
        vim.command(argus)
        return 0

    def all_types(self):
        # return all vim objects
        # 1. windows
        # 2. tabpages
        # 3. buffers
        wyn = vim.windows
        buf = vim.buffers
        tab = vim.tabpages
        return (wyn, buf, tab)

env = VimObject()


class VIMRPCENV(object):
    """VIMRPCENV Enviroment
    This Class Contains all
    The API accessible to the Rpc Client.
    Functions that start with '_' for security
    reason are not accessible to the Client

    # CURRENTLY SUPPORTRD PROTOCOLS ARE JSON & XML"""

    def __init__(self,):
        # INIT class Variables
        self.restr = os.path.expanduser('~/.vim/fakepid.VimRpc')
        # self.restr the empty file vim opens when running as
        # a "daemon" should not be edited
        self.classes = ['VIMRPCENV']
        self.funcs = []
        self.id = 0
        self.RESULT = {'ID': self.id, 'Result': '', 'Error': ''}

    def _resolve_d_attr(self, attr, allow_dotted_names=True):
        # avoid Functions that starts with "_"
        attrs = [attr]
        for i in attrs:
            if i.startswith('_'):
                raise AttributeError('\
                attempt to access private attribute "%s"' % i)
            else:
                obj = getattr(self, i)
        return obj

    def _strtowin(self, win):
        """convert string to vim window object"""
        mywins, _, _ = env.all_types()
        fake = self.getWindows()
        no = fake.index(win)
        real = mywins[no]
        return real

    def _dispatch(self, method, params):
        # only used for XML PROTOCOL
        func = None
        err_msg = None
        return_value = None
        self.id += 1
        try:
            func = self._resolve_d_attr(
                method,
                allow_dotted_names=True
            )
        except AttributeError:
            err_msg = '''Illegal Permisson to access
                Private Function anf Variables'''
        if func is not None:
            try:
                return_value = func(*params)
            except Exception as e:
                err_msg = str(e).upper()
        else:
            err_msg = 'Unknowm Rpc Code %s() .......' % method
        self._prepare(Ret=return_value, Err=err_msg)
        '''if self.RESULT['Error'] is None:
            return self.RESULT['Result']'''
        return self.RESULT

    def _prepare(self, Ret=None, Err=''):
        # convert return_value to string
        self.RESULT['ID'] = self.id
        self.RESULT['Result'] = Ret
        self.RESULT['Error'] = Err
        return 0

# """ FUNCTIONS HERE CAN BE CALLED BY THE CLIENT"""
# FOR ALL FUNCTIONS HERE RUN ':help VimRpc-API-Functions'
# To Get What they do and what they return
# ======= CALLABLE FUNCTIONS  =============

    def curWin(self):
        return_value = env.curwin()
        if return_value.buffer.name == self.restr:
            return_value = []
        return str(return_value)

    def curWinData(self):
        mywin = vim.current.window.buffer
        return mywin[:]

    def winData(self, win):
        win = self._strtowin(win)
        if win.buffer.name == self.restr:
            raise vim.errro('CANNOT GET BUILTIN WIN DATA')
        return win.buffer[:]

    def writeWin(self, win=None):
        if win is None:
            win = env.curwin()
        else:
            win = self._strtowin(win)
        real = win
        if real.buffer.name == self.restr:
            raise vim.errro('cannot write builtin buff')
        vim.current.window = real
        env.do('write')
        return_value = 0
        return return_value

    def substitute(self, patttern, string, Range='g'):
        return_no = 0
        myfunc = vim.Function('substitute')
        new_win = env.curbuf()[:]
        no = 0
        for line in new_win:
            value = myfunc(line, patttern, string, Range)
            value = value.decode()
            new_win[no] = value
            no += 1
            if value != line:
                return_no += 1
        vim.current.buffer[:] = new_win
        return return_no

    def match(self, string, start=0):
        buffer = self.curWinData()
        match_obj = vim.Function('match')
        return_no = match_obj(buffer, string, start)
        return return_no

    def search(self, patttern, flag=None):
        self.normalCommand('gg')
        no = 0
        strings = self.curWinData()
        return_str = []
        lines = len(strings)
        func = vim.Function('search')
        if flag is None:
            flag = 'c'
        while no <= lines:
            no += 1
            myeval = func(patttern, )
            if myeval == 0:
                break
            myeval -= 1
            if strings[myeval] in return_str:
                continue
            return_str.append(strings[myeval])
        self.normalCommand('gg')
        return return_str

    def insert(self, line, data):
        if line == 0:
            raise vim.error('INVALID LINE NUMBER')
        if type(data) is str:
            data = [data]
        data.reverse()
        old = env.curbuf()
        old = old[:]
        line = int(line) - 1
        for mys in data:
            old.insert(line, mys)
        vim.current.buffer[:] = old
        return 0

    def append(self, data):
        if type(data) is str:
            data = [data]
        line = vim.current.buffer
        for strin in data:
            line.append(strin)
        return 0

    def prevWin(self):
        mywins, _, _ = env.all_types()
        fake = self.getWindows()
        old_win = str(env.curwin())
        no = fake.index(old_win) - 1
        if no == -1:
            raise vim.error('NO Such WINDOW')
        formal_win = mywins[no]
        if formal_win.buffer.name == self.restr:
            raise vim.error('%s IS THE FIRST WINDOW\
                            ...' % old_win.buffer.name)
        vim.current.window = formal_win
        return 0

    def nextWin(self):
        mywins, _, _ = env.all_types()
        fake = self.getWindows()
        old_win = str(env.curwin())
        no = fake.index(old_win) + 1
        new_win = mywins[no]
        vim.current.window = new_win
        return 0

    def moveToWin(self, win):
        real = self._strtowin(win)
        env.move(1, 0, win=real)
        return 0

    def normalCommand(self, comm):
        if comm == 'ZZ':
            raise RuntimeError("Cannot Close window with 'ZZ' try using\
                               VimRpc.CloseWin(win)")
        comm = 'normal ' + str(comm)
        self.exCommand(comm)
        return 0

    def fCloseWin(self, win):
        real_win = self._strtowin(win)
        if real_win.buffer.name == self.restr:
            raise vim.error('Cannot Close BUILTIN Window')
        env.move(1, 0, win=real_win)
        env.do('q!')
        return 0

    def wCloseWin(self, win):
        real_win = self._strtowin(win)
        if real_win.buffer.name == self.restr:
            raise vim.error('Cannot Close BUILTIN Window')
        env.move(1, 0, win=real_win)
        env.do('close')
        return 0

    def wCloseAll(self):
        mywins, _, _ = env.all_types()
        old = env.curwin()
        if old.buffer.name == self.restr:
            raise vim.error('NO USER AVAILABLE BUFFER')
        num = 0
        for win in mywins:
            if win.buffer.name == self.restr:
                continue
            env.move(1, 0, win=win)
            env.do('wq!')
            num += 1
        vim.current.window = old
        return num

    def fCloseAll(self,):
        mywins, _, _ = env.all_types()
        old = env.curwin()
        if old.buffer.name == self.restr:
            raise vim.error('NO AVAILABLE BUFFER')
        num = 0
        for win in mywins:
            if win.buffer.name == self.restr:
                continue
            env.move(1, 0, win=win)
            env.do('q!')
            num += 1
        vim.current.window = old
        return num

    def getWindowName(self, win=None):
        if win is None:
            return vim.current.window.buffer.name
        real_win = self._strtowin(win)
        return real_win.buffer.name

    def getAllWindowNames(self):
        mywins, _, _ = env.all_types()
        data = []
        for i in mywins:
            if i.buffer.name == self.restr:
                continue
            data.append(i.buffer.name)
        return data

    def openFile(self, mfile):
        mfile = path.expanduser(mfile)
        env.do('new %s' % mfile)
        return str(env.curwin())

    def getWindows(self,):
        mybuffs, _, _ = env.all_types()
        mast = []
        for b in mybuffs:
            if b.buffer.name == self.restr:
                continue
            mast.append(str(b))
        return mast

    def getLine(self, line, win=None):
        env.move(line, 0)
        minst = env.curbuf()
        return_value = minst[line-1]
        splited = return_value.strip()
        env.move(1, 0)
        return splited

    def eval(self, data):
        minst = env.eval(data)
        return minst

    def exCommand(self, command):
        no_dict = ('wqa', 'wqall!', 'qall!', 'qa', 'wa', 'wall',
                   'wal!', 'quit!', 'quit', 'quitall!', 'quitall',
                   'write', 'write!')
        list_com = command.split(' ')
        first = list_com[0]
        if first in no_dict:
            raise vim.error('cannot run command %s try using THE API FUNCTIONS'
                            % command)
        return vim.command(command)

    def vimFunction(self, func, args=()):
        myfunc = vim.Function(func)
        eval = myfunc(*args)
        eval = eval.decode()
        return eval

    def closeCurwin(self, force=False):
        if force is False:
            self.wCloseWin(str(env.curwin()))
        elif force is True:
            self.fCloseWin(str(env.curwin()))
        else:
            raise RuntimeError("Unknowm option %s " % force)
        return 0

master = VIMRPCENV()
