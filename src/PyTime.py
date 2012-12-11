#!/usr/bin/env python
'''
Created on Oct 28, 2012

@author: Christoph Graupner
'''
from Listener import Mate
from Store.Sqlite import Sqlite
import time
import os
import pwd
from datetime import timedelta
import Gui.Mate

class PyTime:
    def __init__(self):
        self._store = Sqlite(os.path.join(os.path.expanduser("~"), '.PyTime', "user." + pwd.getpwuid(os.getuid())[0] + ".test.sqlite"))
        self._eventSource = Mate.Mate()
    
    def runGui(self):
        self._gui = Gui.Mate.Mate()
        self._gui.run()
    
    def startLogger(self):
        self._eventSource = Mate.Mate()
        lTime = time.gmtime()
        print "Start", time.strftime("%Y%m%dT%H%M%S+0000", lTime), "Uptime: ", self.uptime()
        self._eventSource.registerForLock(self.callbackLock)
        self._eventSource.registerForUnlock(self.callbackUnlock)
        self._store.write(lTime, "started")
        self._eventSource.start()
        
    def stopLogger(self):
        self._eventSource.stop()
        self._store.write(time.gmtime(), "stopped")
   
    def run(self):
        try:
            self.startLogger()
            self.runGui()
            self.stopLogger()

        except KeyboardInterrupt:
            lTime = time.gmtime()
            print "Stopped", time.strftime("%Y%m%dT%H%M%S+0000", lTime)
            self._store.write(lTime, "user_interupt")
        except:
            self._store.write(time.gmtime(), "unexpected_end")
            raise
        
    def callbackLock(self):
        lTime = time.gmtime()
        print "Locked: " , time.strftime("%Y%m%dT%H%M%S+0000", lTime)
        self._store.write(lTime, "lock")
        
    def callbackUnlock(self):
        lTime = time.gmtime()
        print "Unlocked", time.strftime("%Y%m%dT%H%M%S+0000", lTime)
        self._store.write(lTime, "unlock")
        
    def uptime(self):
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))
            return uptime_string

if __name__ == '__main__':
    pyTime = PyTime()
    pyTime.run()
