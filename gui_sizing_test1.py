import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

def print_size(widget, data=None):
    print widget.get_size()

def delete_event(widget, data=None):
    print widget.get_size()
    return False

def destroy(widget, data=None):
    Gtk.main_quit()

class testwin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="ASD")
        self.maximize()


class mainwin(Gtk.Window):
    def __init__(self,screen):
        Gtk.Window.__init__(self,title="Ghetto OMR")
        main = Gtk.Label("ASDASD")
        self.add(main)
        curr_screen=screen.get_active_window()
        self.win_height=curr_screen.get_height()
        self.win_width = curr_screen.get_width()
        self.set_screen(screen)
        self.resize(self.win_width,self.win_height)




cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
# With the others GTK_STYLE_PROVIDER_PRIORITY values get the same result

testwin = testwin()
testwin.connect('delete_event', delete_event)
testwin.connect('destroy', destroy)
testwin.show_all()

win = mainwin(screen)
# win.connect("delete-event",Gtk.main_quit)
win.connect('delete_event', delete_event)
win.connect('destroy', destroy)
win.show_all()
Gtk.main()