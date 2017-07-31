import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ToggleButtonWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="ToggleButton Demo")
        self.set_border_width(10)

        self.vbox = Gtk.VBox(spacing=6)
        self.vbox = Gtk.Box(spacing=6)
        self.add(self.vbox)

        self.button1 = Gtk.ToggleButton()
        self.button1.connect("toggled", self.on_button_toggled, "1")
        self.button1.set_active(True)
        self.button1img = Gtk.Image.new_from_icon_name("filenew",Gtk.IconSize.MENU)
        self.button1.set_image(self.button1img)

        self.vbox.pack_start(self.button1, True, True, 0)

        self.button2 = Gtk.ToggleButton("Button 2")
        self.button2.connect("toggled", self.on_button_toggled, "2")
        self.vbox.pack_start(self.button2, True, True, 0)

        self.button3 = Gtk.ToggleButton("Button 3")
        self.button3.connect("toggled", self.on_button_toggled, "3")
        self.vbox.pack_start(self.button3, True, True, 0)


    def on_button_toggled(self, button, name):

        if button.get_active():             # this part is to deactivate all button when one is activated
            for i in self.vbox:
                if type(i)==Gtk.ToggleButton:
                    if i !=button:
                        i.set_active(False)
        else:
            k=0                     #this part is to activate button 1 when all is deactivated
            for i in self.vbox:
                if type(i)==Gtk.ToggleButton:
                    m=i.get_active()
                    k=k+m
            if k ==0:
                self.button1.set_active(True)


win = ToggleButtonWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()