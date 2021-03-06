"""
Created on Nov 30, 2012

@author: Christoph Graupner <ch.graupner@workingdeveloper.de>
"""
import time

import gtk
from Gui import Abstract
import Gui
import inspect, os
#from gi.repository import GObject
from Events import EventManager


class Mate(Abstract):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        self._window = None
        Gui.Abstract.__init__(self)

    def create(self):
        self._listeners = {"quit"}
        self._window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self._window.connect("delete_event", self.onWindowDelete)
        self._window.connect("destroy", self.onWindowDestory)
        self._window.set_border_width(10)
        self._btnQuit = gtk.Button("Quit")
        self._btnQuit.connect("clicked", self.onQuitClick, None)
        self._btnQuit.connect_object("clicked", gtk.Widget.destroy, self._window)
        self._window.add(self._btnQuit)
        self._btnQuit.show()
        self._statusIcon = StatusIcon(self._window)

        #self._window.show()

    def onQuitClick(self, widget, data=None):
        EventManager.i().emitAppQuit(self, "quit click")
        gtk.main_quit()

    def onWindowDestory(self, widget, data=None):
        EventManager.i().emitAppQuit(self, "window destroy")
        gtk.main_quit()

    def onWindowDelete(self, widget, data=None):
        return False

    def askReason(self, title, predefined):
        dlg = StatusInputDialog(title, predefined)
        dlg.run()

    def run(self):
        if self._window is None:
            self.create()
        gtk.main()


class StatusIcon():
    def __init__(self, window):
        self.statusicon = gtk.StatusIcon()
        icon = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        icon = os.path.join(os.path.dirname(icon), 'resources', 'icon22.png')
        self.statusicon.set_from_file(icon)
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
        quit.connect("activate", self.onQuit)
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

    def logStart(self, widget):
        EventManager.i().emitAppRequestEvent(self,
                                             {'event': 'started', 'request': 'log.start', 'reason': 'manual entry',
                                              'time': time.gmtime()})

    def logStop(self, widget):
        EventManager.i().emitScreenUnlock('test unlock')
        # EventManager.i().emitAppRequestEvent(self,
        #                                      {'event': 'stopped', 'request': 'log.stop', 'reason': 'manual entry',
        #                                       'time': time.gmtime()})

    def onQuit(self, widget):
        gtk.main_quit()
        EventManager.i().emitAppQuit(self, "GUI: user request")


class AboutDialog(object):
    def __init__(self):
        self._dlg = gtk.AboutDialog()
        self._dlg.set_destroy_with_parent(True)
        self._dlg.set_name("WorkingDevelopers PyTime")
        self._dlg.set_version("1.2")
        self._dlg.set_authors(["Christoph Graupner"])

    def run(self):
        self._dlg.run()
        self._dlg.destroy()


class StatusInputDialog(gtk.Dialog):
    def __init__(self, title, predefined):
        super(StatusInputDialog, self).__init__(buttons=('OK', 1, 'Cancel', 0))
        self.set_title(title)
        self.set_flags(gtk.DIALOG_DESTROY_WITH_PARENT)

        self.set_size_request(250, 100)
        self.set_position(gtk.WIN_POS_CENTER)
        # self.connect("destroy", gtk.)

        table = gtk.Table(2, 2, True)

        info = gtk.Button("Information")
        warn = gtk.Button("Warning")
        ques = gtk.Button("Question")
        erro = gtk.Button("Error")

        info.connect("clicked", self.on_info)
        warn.connect("clicked", self.on_warn)
        ques.connect("clicked", self.on_ques)
        erro.connect("clicked", self.on_erro)

        table.attach(info, 0, 1, 0, 1)
        table.attach(warn, 1, 2, 0, 1)
        table.attach(ques, 0, 1, 1, 2)
        table.attach(erro, 1, 2, 1, 2)
        # self.action_area.pack_start(info, 1, 1, 0)
        # self.add_button('info',info)

        self.vbox.add(table)
        self.show_all()

    def on_info(self, widget):
        md = gtk.MessageDialog(self,
                               gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                               gtk.BUTTONS_CLOSE, "Download completed")
        md.run()
        md.destroy()


    def on_erro(self, widget):
        md = gtk.MessageDialog(self,
                               gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
                               gtk.BUTTONS_CLOSE, "Error loading file")
        md.run()
        md.destroy()


    def on_ques(self, widget):
        md = gtk.MessageDialog(self,
                               gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION,
                               gtk.BUTTONS_CLOSE, "Are you sure to quit?")
        md.run()
        md.destroy()


    def on_warn(self, widget):
        md = gtk.MessageDialog(self,
                               gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING,
                               gtk.BUTTONS_CLOSE, "Unallowed operation")
        md.run()
        md.destroy()