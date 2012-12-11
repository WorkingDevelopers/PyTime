class ListenerAbstract():
    
    def __init__(self):
        self._listenersLock = []
        self._listenersUnlock = []
    
    def start(self):
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
