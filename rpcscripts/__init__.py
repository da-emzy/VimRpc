#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from threading import Thread


class ModThread(Thread):
    """modified thread object."""
    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except OSError:
                pass
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
