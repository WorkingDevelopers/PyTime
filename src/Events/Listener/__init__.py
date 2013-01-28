"""
signal sender=:1.116 -> dest=(null destination) serial=21 path=/org/gnome/ScreenSaver; interface=org.gnome.ScreenSaver; member=ActiveChanged
   boolean false
signal sender=:1.0 -> dest=(null destination) serial=92 path=/org/gnome/SessionManager/Presence; interface=org.gnome.SessionManager.Presence; member=StatusChanged
   uint32 0

@author Christoph Graupner <ch.graupner@workingdeveloper.de>
"""


class ListenerScreen():
    def onLock(self, sender=None):
        pass

    def onUnlock(self, sender=None):
        pass

    def onExit(self, sender=None):
        pass


class ListenerApplication():
    def onQuit(self, sender=None, reason=None):
        pass

    def onStart(self, sender=None):
        pass

class ListenerLog():
    def requestLog(self, message, sender=None):
        pass

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
