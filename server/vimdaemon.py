#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Generic linux daemon base class for python """

import sys
import os
import time
import atexit
import signal

vimfake = os.path.expanduser('~/.vim/fakepid.VimRpc')


class MyDaemon():
    """A generic daemon class.

    Usage: subclass the daemon class and override the run() method."""

    def __init__(self, pidfile='/tmp/hullht.pid'):
        self.pidfile = pidfile
        os.environ.putenv('VIM_PID_F', self.pidfile)

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:

                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        """si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        s.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())"""

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile, 'w') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon."""

        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pf:

                pid = pf.readlines()
        except IOError:
            pid = None

        if pid:
            message = "pidfile {0} already exist. " + \
                            "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def status(self):
        """Get the Current Status of the Daemon"""
        try:
            with open(self.pidfile, 'r') as pf:

                pid = pf.readlines()
        except IOError:
            pid = None
        if not pid:
            message = "Daemon Not Running.....\n"
        elif pid:
            message = "Vim Daemon Running...................\n"
        sys.stdout.write(message)

    def stop(self):
        """Stop the daemon."""

        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pids = pf.readlines()
                d_pid = pids[0].strip()
                v_pid = pids[1].strip()
                d_pid, v_pid = int(d_pid), int(v_pid)
        except IOError:
            pids = None

        if not pids:
            message = "Cannot find Daemon pidfile {0} " + \
                            "Daemon not running......\n"
            sys.stderr.write(message.format(self.pidfile))
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(v_pid, signal.SIGTERM)
                os.kill(d_pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
                message = " Killing VimRpc Daemon......\n"
                sys.stdout.write(message)
                sys.stdout.flush()
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        """Run Vim daemon"""
        if os.path.isfile(vimfake):
            os.remove(vimfake)
        """This stuff is reaaaaally a naive hack! I cannot stress enough, that
        this is a stupid solution.
        But there is really no other yet and this seems to work,
        There is no possibility yet to make VIM run as a daemon and not
        write to /dev/tty. except patching the source file.
        but when a better alternative comes it would be implemented
        (:help VimRpc-Development on how to contribute)
        (Da Emzy, 2017 July 14)"""
        os.system('vim %s > /dev/null' % vimfake)
        sys.stdout.write("STARTING VIM DAEMON........\n")
        sys.stdout.flush()
        while True:  # since the  daemon needs to keep running
            pass  # we need to keep the while loop and do nothing.

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/hullht.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print("Unknown command ")
            print("usage: %s start|stop|restart " % sys.argv[0])
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart " % sys.argv[0])
        sys.exit(2)
