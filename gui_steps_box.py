import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import numpy as np
import obj_func

class widget_list:
    def __init__(self):
        self.list = []
        self.counter = 0
    def add(self,widget):
        self.list.append(widget)
        self.counter = self.counter + 1

class step_grid(Gtk.Grid):
    def __init__(self,main_grid):
        Gtk.Grid.__init__(self)
        self.maingrid = main_grid
        self.n_row = 0
        self.set_row_spacing(2)
        self.widgetlist = widget_list()

        button1 = step_box("browser",self)
        self.add(button1)

        button2 = step_box("alienarena",self)
        self.add(button2)

        button3 = step_box("live",self)
        self.add(button3)

        button4 = step_box("cs-network",self)
        self.add(button4)

    def add(self,widget):
        self.attach(widget,0,self.n_row,1,1)
        self.n_row = self.n_row +1
        widget.num = self.n_row
        self.widgetlist.add(widget)

class content_box(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        self.content = None
        self.set_size_request(300,300)

    def set_new(self,name):
        # if self.content != None:
        #     self.content.destroy()
        obj_dict = {"browser": obj_func.func0,
                     "alienarena": obj_func.func1,
                     "live": obj_func.func2,
                     "cs-network": obj_func.func3
                     }

        obj_func_exist = name in obj_dict
        if obj_func_exist:
            self.content = obj_dict[name]()
            self.set_center_widget(self.content)

class main_grid(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.contentbox = content_box()
        stepgrid = step_grid(self)

        self.attach(stepgrid,0,0,1,1)
        self.attach(self.contentbox,0,1,1,1)


class step_box(Gtk.EventBox):
    def __init__(self,label_str,parent):
        Gtk.EventBox.__init__(self)
        self.num = -1
        self.stepgrid = parent
        self.label = label_str
        some_label = Gtk.Label(label_str)
        self.add(some_label)
        self.connect("button-press-event",self.on_button_press)

    def on_button_press(self,widget,event):
        # tool_dict = {"browser": step_func.func0,
        #              "alienarena": step_func.func1,
        #              "live": step_func.func2,
        #              "cs-network": step_func.func3
        #              }

        button_pressed = event.button
        a=widget.label

        if button_pressed ==1:
            self.stepgrid.maingrid.contentbox.set_new(a)
            if widget.get_state()==Gtk.StateType.NORMAL:
                #set clicked to selected
                for widgets in self.stepgrid.widgetlist.list:
                    if widgets.get_state()==Gtk.StateType.SELECTED:
                        widgets.set_state(Gtk.StateType.NORMAL)
                        Gtk.StyleContext.remove_class(widgets.get_style_context(), "highlighted")

                Gtk.StyleContext.add_class(widget.get_style_context(), "highlighted")
                widget.set_state(Gtk.StateType.SELECTED)



class mainwin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        somegrid = main_grid()



        self.add(somegrid)

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,Gtk.STYLE_PROVIDER_PRIORITY_USER)

win = mainwin()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()