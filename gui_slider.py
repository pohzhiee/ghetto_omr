import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class slider(Gtk.Scale):
    def __init__(self):
        Gtk.HScale.__init__(self)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_range(0,1000)
        self.set_value_pos(Gtk.PositionType.TOP)
        self.set_increments(1,1)
        self.set_digits(0)
        self.set_draw_value(False)
        self.connect("change-value",self.func1)

    def func1(self,widget,some_enum,new_val):
        print ("Value changed to",new_val)


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        slid = slider()
        self.set_default_size(500,300)
        self.add(slid)

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.maximize()
win.show_all()
Gtk.main()