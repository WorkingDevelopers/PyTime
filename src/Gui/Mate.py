'''
Created on Nov 30, 2012

@author: christoph
'''
import gtk
from Gui import Abstract
#from gi.repository import GObject

class Mate(Abstract):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._window = None
        
    def create(self):
        self._window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self._window.connect("delete_event",self.onWindowDelete)
        self._window.connect("destroy",self.onWindowDestory)
        self._window.set_border_width(10)
        self._btnQuit = gtk.Button("Quit")
        self._btnQuit.connect("clicked",self.onQuitClick, None)
        self._btnQuit.connect_object("clicked",gtk.Widget.destroy,self._window)
        self._window.add(self._btnQuit)
        self._btnQuit.show()
        self._statusIcon = StatusIcon(self._window)

        #self._window.show()
        
    def onQuitClick(self,widget,data=None):
        print "quit"
        
    def onWindowDestory(self,widget,data=None):
        print "detroyed"
        gtk.main_quit()
        
    def onWindowDelete(self,widget,data=None):
        print "delete"
        return False
        
    def run(self):
        if self._window == None:
            self.create()
        gtk.main()
        
class StatusIcon():
    
    def __init__(self,window):
        self.statusicon = gtk.StatusIcon()
        self.statusicon.set_from_stock(gtk.STOCK_HOME) 
        self.statusicon.connect("popup-menu", self.right_click_event)

    def right_click_event(self, icon, button, time):
        menu = gtk.Menu()

        about = gtk.MenuItem()
        about.set_label("About")
        logStart = gtk.MenuItem()
        logStart.set_label("Log Start")
        logStop = gtk.MenuItem()
        logStop.set_label("Log Stop")
        quit = gtk.MenuItem()
        quit.set_label("Quit")

        about.connect("activate", self.show_about_dialog)
        quit.connect("activate", gtk.main_quit)
        logStart.connect("activate", self.logStart)
        logStop.connect("activate", self.logStop)

        menu.append(about)
        menu.append(logStart)
        menu.append(logStop)
        menu.append(quit)

        menu.show_all()
        menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusicon)

    def show_about_dialog(self, widget):
        about_dialog = AboutDialog()
        about_dialog.run()
        
    def logStart(self,widget):
        pass
    
    def logStop(self,widget):
        pass

class AboutDialog(object):
    def __init__(self):
        self._dlg = gtk.AboutDialog()
        self._dlg.set_destroy_with_parent(True)
        self._dlg.set_name("WorkingDevelopers PyTime")
        self._dlg.set_version("1.0")
        self._dlg.set_authors(["Christoph Graupner"])
        
    def run(self):
        self._dlg.run()
        self._dlg.destroy()
