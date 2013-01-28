__author__ = 'Christoph Graupner <christoph.graupner@workingdeveloper.net'


class EventManager(object):
    EVT_SCREEN_LOCK = "screen.lock"
    EVT_SCREEN_UNLOCK = "screen.unlock"
    EVT_SCREEN_EXIT = "screen.exit"
    EVT_APP_START = "app.start"
    EVT_APP_QUIT = "app.quit"
    EVT_APP_REQUEST_LOG = "app.log.request"

    instances = {}

    @classmethod
    def i(cls):
        """
        @return EventManager
        """
        if cls not in cls.instances:
            cls.instances[cls] = cls()
        return cls.instances[cls]

    def __init__(self):
        self._listeners = {EventManager.EVT_APP_QUIT: [], EventManager.EVT_APP_START: [],
                           EventManager.EVT_SCREEN_LOCK: [], EventManager.EVT_SCREEN_UNLOCK: [],
                           EventManager.EVT_SCREEN_EXIT: [], EventManager.EVT_APP_REQUEST_LOG: []}

    def shutdown(self):
        self._listeners = {EventManager.EVT_APP_QUIT: [], EventManager.EVT_APP_START: [],
                           EventManager.EVT_SCREEN_LOCK: [], EventManager.EVT_SCREEN_UNLOCK: [],
                           EventManager.EVT_SCREEN_EXIT: [], EventManager.EVT_APP_REQUEST_LOG: []}

    def register(self, event, listener):
        if self._listeners.has_key(event):
            self._listeners[event].append(listener)
        else:
            raise Exception("No event " + event + " to register for.")

    def unregister(self, event, listener):
        if self._listeners.has_key(event):
            self._listeners[event].remove(listener)
        else:
            raise Exception("No event " + event + " to register for.")

    def emitScreenLock(self, sender):
        for listener in self._listeners[EventManager.EVT_SCREEN_LOCK]:
            listener.onLock(sender)

    def emitScreenUnlock(self, sender):
        for listener in self._listeners[EventManager.EVT_SCREEN_UNLOCK]:
            listener.onUnlock(sender)

    def emitScreenExit(self, sender):
        for listener in self._listeners[EventManager.EVT_SCREEN_EXIT]:
            listener.onExit(sender)

    def emitAppStart(self, sender):
        for listener in self._listeners[EventManager.EVT_APP_START]:
            listener.onStart(sender)

    def emitAppQuit(self, sender, reason=None):
        for listener in self._listeners[EventManager.EVT_APP_QUIT]:
            listener.onQuit(sender, reason)

    def emitAppRequestEvent(self, sender, message):
        for listener in self._listeners[EventManager.EVT_APP_REQUEST_LOG]:
            listener.requestLog(message, sender)
