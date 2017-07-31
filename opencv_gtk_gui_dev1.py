import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo

class toolbox(Gtk.Grid):
    def __init__(self,parent):
        Gtk.Grid.__init__(self)
        self.set_border_width(10)

        self.vbox = Gtk.VBox(spacing=6)
        self.vbox = Gtk.Box(spacing=6)
        self.add(self.vbox)

        self.button1 = Gtk.ToggleButton("Button1")
        self.button1.connect("toggled", self.on_button_toggled, "1")
        self.button1.set_active(True)
        #self.button1img = Gtk.Image.new_from_icon_name("filenew", Gtk.IconSize.MENU)
        #self.button1.set_image(self.button1img)

        self.vbox.pack_start(self.button1, True, True, 0)

        self.button2 = Gtk.ToggleButton("Button 2")
        self.button2.connect("toggled", self.on_button_toggled, "2")
        self.vbox.pack_start(self.button2, True, True, 0)

        self.button3 = Gtk.ToggleButton("Button 3")
        self.button3.connect("toggled", self.on_button_toggled, "3")
        self.vbox.pack_start(self.button3, True, True, 0)

        self.attach(self.button1, 0, 0, 1, 1)
        self.attach(self.button2, 1, 0, 3, 1)
        self.attach(self.button3, 2, 0, 1, 1)

    def on_button_toggled(self, button, name):

        if button.get_active():  # this part is to deactivate all button when one is activated
            for i in self.vbox:
                if type(i) == Gtk.ToggleButton:
                    if i != button:
                        i.set_active(False)
        else:
            k = 0  # this part is to activate button 1 when all is deactivated
            for i in self.vbox:
                if type(i) == Gtk.ToggleButton:
                    m = i.get_active()
                    k = k + m
            if k == 0:

                self.button1.set_active(True)

class drawingarea(Gtk.DrawingArea):
    def __init__(self,parent):
        Gtk.DrawingArea.__init__(self)
        self.connect("draw",self.on_draw)
        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.coords = []
        self.connect("button-press-event", self.on_button_press)

    def on_draw(self, wid, cr):

        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(0.5)

        for i in self.coords:
            for j in self.coords:
                cr.move_to(i[0], i[1])
                cr.line_to(j[0], j[1])
                cr.stroke()

        del self.coords[:]
    def on_button_press(self, w, e):

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == 1: #Left Button
            self.coords.append([e.x, e.y])

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == 3: #Right Button
            self.queue_draw()


            # class image(Gtk.Image):
#     def __init__(self, parent):
#         x

class sidebox(Gtk.Box):
    def __init__(self,parent):
        Gtk.Box.__init__(self)

        tool = toolbox(self)
        self.add(tool)

class mainbox(Gtk.Box):
    def __init__(self,parent):
        Gtk.Box.__init__(self)
        self.set_hexpand(True)
        drawingA=drawingarea(self)
        # img=image(self)

        self.add(drawingA)
        # self.add(img)

class stepbox(Gtk.Box):
    def __init__(self,parent):
        Gtk.Box.__init__(self)
        b=Gtk.Label("Hello")
        self.set_hexpand(True)

        self.add(b)

class maingrid(Gtk.Grid):
    def __init__(self,parent):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(25)
        step = stepbox(self)
        main= mainbox(self)
        side = sidebox(self)



        self.attach(step, 0, 0, 20, 10)
        self.attach(main, 21, 0, 40, 10)
        self.attach(side, 61, 0, 10, 10)

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Template Design")
        main=maingrid(self)
        self.add(main)
        self.maximize()


win = Window()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()