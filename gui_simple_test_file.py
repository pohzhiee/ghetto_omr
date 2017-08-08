import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk,GdkPixbuf as pixbuf

class RadioButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="RadioButton Demo")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.grid = Gtk.Grid()
        self.textspace1 = Gtk.Entry()
        self.textspace2 = Gtk.Entry()
        self.grid.attach(hbox,0,0,1,1)
        self.grid.attach(self.textspace1,0,1,1,1)
        self.grid.attach_next_to(self.textspace2,self.textspace1,Gtk.PositionType.BOTTOM,1,1)
        self.add(self.grid)

        self.textstr = ""

        button1 = Gtk.RadioButton.new(None)
        button1.connect("toggled", self.on_button_toggled, "1")
        button1.set_mode(False)
        pix = pixbuf.Pixbuf.new_from_file("icons/facebook.svg")
        pix1=pix.scale_simple(40,40,pixbuf.InterpType.BILINEAR)
        img = Gtk.Image.new_from_pixbuf(pix1)
        button1.set_image(img)
        button1.set_relief(Gtk.ReliefStyle.NONE)
        # button1.do_draw_indicator(False,False)
        hbox.pack_start(button1, False, False, 0)

        button2 = Gtk.RadioButton.new_from_widget(button1)
        button2.set_mode(False)
        pix = pixbuf.Pixbuf.new_from_file("icons/live.svg")
        pix1=pix.scale_simple(40,40,pixbuf.InterpType.BILINEAR)
        img = Gtk.Image.new_from_pixbuf(pix1)
        button2.set_image(img)
        button2.connect("toggled", self.on_button_toggled, "2")
        hbox.pack_start(button2, False, False, 0)

        button3 = Gtk.RadioButton.new()
        button3.set_mode(False)
        button3.join_group(button1)
        pix = pixbuf.Pixbuf.new_from_file("icons/cs-cat-hardware.svg")
        pix1=pix.scale_simple(40,40,pixbuf.InterpType.BILINEAR)
        img = Gtk.Image.new_from_pixbuf(pix1)
        button3.set_image(img)
        button3.connect("toggled", self.on_button_toggled, "3")
        hbox.pack_start(button3, False, False, 0)

        button4 = Gtk.RadioButton.new()
        button4.set_mode(False)
        button4.join_group(button1)
        pix = pixbuf.Pixbuf.new_from_file("icons/cs-network.svg")
        pix1=pix.scale_simple(40,40,pixbuf.InterpType.BILINEAR)
        img = Gtk.Image.new_from_pixbuf(pix1)
        button4.set_image(img)
        button4.connect("toggled", self.on_button_toggled,"4")
        hbox.pack_start(button4,False,False,0)

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
            Gtk.StyleContext.add_class(button.get_style_context(), "toggleasd")
        else:
            state = "off"
            Gtk.StyleContext.remove_class(button.get_style_context(),"toggleasd")
        textbuf = self.textstr
        self.textstr = "Button {} was turned {}".format(name,state)
        self.textspace1.set_text(textbuf)
        self.textspace2.set_text(self.textstr)
        # print("Button", name, "was turned", state)

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,Gtk.STYLE_PROVIDER_PRIORITY_USER)

win = RadioButtonWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()