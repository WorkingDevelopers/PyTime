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
import Gui.Mate

class PyTime:
    def __init__(self):
        self._store = Sqlite("user." + pwd.getpwuid(os.getuid())[0] + ".test.sqlite")
    
    def run(self):
        self.startLogger()
        self.runGui()
        self.stopLogger()
        
    def runGui(self):
        self._gui = Gui.Mate.Mate()
        self._gui.run()
    
    def startLogger(self):
        self._eventSource = Mate.Mate()
        self._eventSource.registerForLock(self.callbackLock)
        self._eventSource.registerForUnlock(self.callbackUnlock)
        self._store.write(time.gmtime(), "started")
        self._eventSource.start()
        
    def stopLogger(self):
        self._eventSource.stop()
        self._store.write(time.gmtime(), "stopped")
        
    def callbackLock(self):
        lTime = time.gmtime()
        print "Locked: " , time.strftime("%Y%m%dT%H%M%S", lTime)
        self._store.write(lTime, "lock")
        
    def callbackUnlock(self):
        lTime = time.gmtime()
        print "Unlocked", time.strftime("%Y%m%dT%H%M%S", lTime)
        self._store.write(lTime, "unlock")

if __name__ == '__main__':
    pyTime = PyTime()
    pyTime.run()
