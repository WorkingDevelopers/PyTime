'''
Created on Oct 28, 2012

@author: christoph
'''
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject
from Listener import ListenerAbstract

class Mate(ListenerAbstract):
    '''
    signal sender=:1.37 -> dest=(null destination) serial=11 path=/org/mate/ScreenSaver; interface=org.mate.ScreenSaver; member=ActiveChanged
   boolean true
   
    classdocs
    '''
    
    STATUS_AVAILABLE = 0
    STATUS_INVISIBLE = 1
    STATUS_BUSY = 2
    STATUS_IDLE = 3

    def __init__(self):
        ListenerAbstract.__init__(self)
        self._loop = None
        self._bus = None
        self._screenInterface = None
        '''signal sender=:1.39 -> dest=(null destination) serial=14 path=/org/mate/ScreenSaver; interface=org.mate.ScreenSaver; member=ActiveChanged
   boolean true

        signal sender=:1.39 -> dest=(null destination) serial=15 path=/org/mate/ScreenSaver; interface=org.mate.ScreenSaver; member=ActiveChanged
   boolean false
s
        Constructor
        '''
        pass
    def initLoop(self):
        DBusGMainLoop(set_as_default=True)
        self._bus = dbus.SessionBus() 
    
    def run(self):
        self.initLoop()
        self.connect()
        self._loop = gobject.MainLoop()
        self._loop.run()
        
    def connect(self):
        self._bus.add_signal_receiver(self.signalHandler, dbus_interface="org.mate.SessionManager.Presence", member_keyword="StatusChanged")
#        self._toggle = True
#        self._bus.add_signal_receiver(self.signalHandlerTest, dbus_interface="org.kde.kglobalaccel.Component", member_keyword="globalShortcutPressed")

#    def signalHandlerTest(self, status, a2, a3, **kwargs):
#        if self._toggle:
#            self.handleUnlock()
#        else:
#            self.handleLock()
#        self._toggle = not self._toggle

        #signal sender=:1.0 -> dest=(null destination) serial=66 path=/org/mate/SessionManager/Presence; interface=org.mate.SessionManager.Presence; member=StatusChanged uint32 3
    def signalHandler(self, status, **kwargs):
        if status == self.STATUS_AVAILABLE:
            self.handleUnlock()
        elif status == self.STATUS_IDLE:
            self.handleLock()
    
