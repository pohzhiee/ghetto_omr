import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import math

class obj0(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.n_col = 2
        self.widget_count = 0

        self.set_column_spacing(2)
        self.set_row_spacing(2)

        button1 = toolbutton("browser")
        self.add(button1)

        button2 = toolbutton("alienarena")
        self.add(button2)

        button3 = toolbutton("live")
        self.add(button3)

        button4 = toolbutton("cs-network")
        self.add(button4)

    def add(self, widget):

        row_num = math.floor(self.widget_count / self.n_col)
        col_num = self.widget_count % self.n_col

        if self.widget_count == 0:
            self.first_radio = widget
        else:
            widget.join_group(self.first_radio)

        self.attach(widget, col_num, row_num, 1, 1)
        self.widget_count = self.widget_count + 1

class toolbutton(Gtk.RadioButton):
    def __init__(self, name):
        Gtk.RadioButton.__init__(self)
        self.name = name
        self.set_mode(False)
        self.connect("toggled", self.tool_btn_toggled)
        self.set_mode(False)
        self.set_relief(Gtk.ReliefStyle.NONE)

        file_path = "icons/" +name + ".svg"
        pix = GdkPixbuf.Pixbuf.new_from_file(file_path)
        pix1=pix.scale_simple(35,35,GdkPixbuf.InterpType.BILINEAR)
        img = Gtk.Image.new_from_pixbuf(pix1)
        self.set_image(img)

    def tool_btn_toggled(self,button):
        if button.get_active():
            state = "on"
            Gtk.StyleContext.add_class(button.get_style_context(), "toggleasd")
        else:
            state = "off"
            Gtk.StyleContext.remove_class(button.get_style_context(), "toggleasd")

        # print(button.name, "has been turned", state)


def func0():
    someobj = obj0()
    print ("FUNC0 ran")
    return someobj

def func1():
    someobj = Gtk.Label("FUNCTION2")
    print ("func1 ran")
    return someobj


def func2():
    someobj = Gtk.Label("FUNCTION3")
    print ("func2 ran")
    return someobj


def func3():
    someobj = Gtk.Label("FUNCTION4")
    print ("func3 ran")
    return someobj