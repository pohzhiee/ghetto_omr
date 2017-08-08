import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from gui_template import tool_func
import math

#Usage:
#when calling toolgrid object number of columns for icons must be defined, number of rows is unlimited

#when creating toolbutton, icon name = toolbutton name
#change folder if necessary

#toolbutton functions are done using dictionary, to be called from function file
#toolbutton function dictionary found inside the class


class toolgrid(Gtk.Grid):
    def __init__(self, n_col):
        Gtk.Grid.__init__(self)
        self.n_col = n_col
        self.widget_count = 0

        self.set_column_spacing(2)
        self.set_row_spacing(2)

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
        tool_dict = {"browser": tool_func.func0,
                     "alienarena": tool_func.func1,
                     "live": tool_func.func2,
                     "cs-network": tool_func.func3
                     }
        if button.get_active():
            state = "on"
            Gtk.StyleContext.add_class(button.get_style_context(), "toggleasd")
            btn_func_exist = button.name in tool_dict
            if btn_func_exist:
                tool_dict[button.name](button.name)
        else:
            state = "off"
            Gtk.StyleContext.remove_class(button.get_style_context(), "toggleasd")

        # print(button.name, "has been turned", state)

class mainwin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        somegrid = toolgrid(2)

        button1 = toolbutton("browser")
        somegrid.add(button1)

        button2 = toolbutton("alienarena")
        somegrid.add(button2)

        button3 = toolbutton("live")
        somegrid.add(button3)

        button4 = toolbutton("cs-network")
        somegrid.add(button4)


        self.add(somegrid)

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('gui_template/tool_button.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,Gtk.STYLE_PROVIDER_PRIORITY_USER)

win = mainwin()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()