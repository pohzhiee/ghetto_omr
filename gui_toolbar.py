import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import numpy as np


#
# class filler_cont_box(Gtk.Box):
#     def __init__(self,row_num,col_num):
#         Gtk.Box.__init__(self):
#         self.str = str(row_num)+","+str(col_num)

class filler_cont(Gtk.Toolbar):
    def __init__(self):
        Gtk.Toolbar.__init__(self)
        button1 = Gtk.ToolButton()
        button1.set_icon_name("")


class some_grid(Gtk.Grid):
    def __init__(self):


class mainwin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        somegrid = some_grid()
        self.add(somegrid)


cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
# With the others GTK_STYLE_PROVIDER_PRIORITY values get the same result
win = mainwin()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()