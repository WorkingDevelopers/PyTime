#!/usr/bin/env python
"""
Created on Oct 28, 2012

@author: Christoph Graupner <ch.graupner@workingdeveloper.de>
"""
import argparse
import atexit
from Store.Sqlite import Sqlite
import time
import os
import pwd
import signal
import sys
from datetime import timedelta
import Gui.Mate
from Events import EventManager
from Events.Listener import Mate, ListenerScreen, ListenerApplication, ListenerLog


class PyTimeController:
    class Listener(ListenerScreen, ListenerApplication, ListenerLog):
        def __init__(self, store, gui):
            self._store = store
            self._gui = gui

        def onLock(self, sender=None):
            lTime = time.gmtime()
            print "Locked: ", time.strftime("%Y%m%dT%H%M%S+0000", lTime)
            self._store.write(lTime, "lock")

        def onStart(self, sender=None):
            ltimesec = time.time()
            lTime = time.gmtime(ltimesec)
            uptime = PyTimeController.uptime()
            timeatup = time.gmtime(ltimesec - uptime)
            print "Start", time.strftime("%Y%m%dT%H%M%S+0000", lTime), " timezone ", str(time.timezone / 3600)
            print "Startup Time", time.strftime("%Y%m%dT%H%M%S+0000", timeatup), "Uptime: ", str(
                timedelta(seconds=uptime))
            self._store.write(timeatup, "timeup-started")
            self._store.write(lTime, "started")

        def onQuit(self, sender=None, reason=None):
            lTime = time.gmtime()
            if reason:
                print "Quit (", reason, ")", time.strftime("%Y%m%dT%H%M%S+0000", lTime)
            else:
                print "Quit", time.strftime("%Y%m%dT%H%M%S+0000", lTime)
                self._store.write(lTime, "stopped")
            self._store.write(lTime, "stopped", reason)


        def onExit(self, sender=None):
            lTime = time.gmtime()
            print "Screen exit", time.strftime("%Y%m%dT%H%M%S+0000", lTime)
            self._store.write(lTime, "screen exit")

        def onUnlock(self, sender=None):
            lTime = time.gmtime()
            reason = self._gui.askReason("Reason for lock", ['Toilet', 'Lunch'])
            print "Unlocked", time.strftime("%Y%m%dT%H%M%S+0000", lTime)
            self._store.write(lTime, "unlock")

        def requestLog(self, message, sender=None):
            print message
            self._store.write(message['time'], message['event'], message['reason'])

    def __init__(self):
        self._store = Sqlite(
            os.path.join(os.path.expanduser("~"), '.PyTime', "user_test." + pwd.getpwuid(os.getuid())[0] + ".sqlite"))
        self._eventSource = Mate.Mate()
        self._gui = Gui.Mate.Mate()
        self._listener = PyTimeController.Listener(self._store, self._gui)
        EventManager.i().register(EventManager.EVT_SCREEN_LOCK, self._listener)
        EventManager.i().register(EventManager.EVT_SCREEN_UNLOCK, self._listener)
        EventManager.i().register(EventManager.EVT_APP_QUIT, self._listener)
        EventManager.i().register(EventManager.EVT_SCREEN_EXIT, self._listener)
        EventManager.i().register(EventManager.EVT_APP_REQUEST_LOG, self._listener)
        EventManager.i().register(EventManager.EVT_APP_START, self._listener)
        atexit.register(self.atexit_handler)

    def atexit_handler(self):
        EventManager.i().emitAppQuit(EventManager.EVT_APP_QUIT, 'at_exit')

    def runGui(self):
        self._gui.run()

    def startLogger(self):
        self._eventSource = Mate.Mate()
        self._eventSource.start()

    def stopLogger(self):
        self._eventSource.stop()

    def run(self):
        try:
            EventManager.i().emitAppStart(self)
            self.startLogger()
            self.runGui()
            self.stopLogger()
            EventManager.i().emitAppQuit(self, "app shutdown")

        except KeyboardInterrupt:
            lTime = time.gmtime()
            EventManager.i().emitAppQuit(self, "user_interupt")
        except:
            EventManager.i().emitAppQuit(self, "unexpected_end")
            raise

    def parseOptions(self):
        parser = argparse.ArgumentParser(description='Setup the SHOP dev-base VM')
        parser.add_argument('-d', '--debug', type=bool, action="store_true",
                            help='Enable debug ')
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-v", "--verbose", action="store_true")
        group.add_argument("-q", "--quiet", action="store_true")
        args = parser.parse()
        if args.debug:
            self.store = Sqlite(os.path.join("debug.user." + pwd.getpwuid(os.getuid())[0] + ".sqlite"))

    @classmethod
    def uptime(cls):
        with open('/proc/uptime', 'r') as f:
            return float(f.readline().split()[0])


if __name__ == '__main__':
    pyTime = PyTimeController()
    pyTime.run()
