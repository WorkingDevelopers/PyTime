'''
signal sender=:1.116 -> dest=(null destination) serial=21 path=/org/gnome/ScreenSaver; interface=org.gnome.ScreenSaver; member=ActiveChanged
   boolean false
signal sender=:1.0 -> dest=(null destination) serial=92 path=/org/gnome/SessionManager/Presence; interface=org.gnome.SessionManager.Presence; member=StatusChanged
   uint32 0

'''

class ListenerAbstract():
    
    def __init__(self):
        self._listenersLock = []
        self._listenersUnlock = []
    
    def run(self):
        pass
    
    def registerForLock(self, callback):
        self._listenersLock.append(callback)
        
    def registerForUnlock(self, callback):
        self._listenersUnlock.append(callback)
        
    def unregisterForUnlock(self, callback):
        pass
    
    def unregisterForLock(self, callback):
        pass

    def handleUnlock(self):
        for listener in self._listenersUnlock:
            listener()
    
    def handleLock(self):
        for listener in self._listenersLock:
            listener()
