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
        self._store = Sqlite("user." + pwd.getpwuid(os.getuid())[0] + ".sqlite")
        self._eventSource = Mate.Mate()
    
    def run(self):
        print "RUN"
        self._store.write(time.gmtime(), "started")
        self._eventSource.registerForLock(self.callbackLock)
        self._eventSource.registerForUnlock(self.callbackUnlock)
        self._eventSource.run()
        
    def callbackLock(self):
        lTime = time.gmtime()
        print "Locked: " , time.strftime("%Y%m%dT%H%M%S",lTime)
        self._store.write(lTime, "lock")
        
    def callbackUnlock(self):
        lTime = time.gmtime()
        print "Unlocked", time.strftime("%Y%m%dT%H%M%S",lTime)
        self._store.write(lTime, "unlock")

if __name__ == '__main__':
    gui = Gui.Mate.Mate()
    gui.run()
#    pyTime = PyTime()
#    pyTime.run()
    
