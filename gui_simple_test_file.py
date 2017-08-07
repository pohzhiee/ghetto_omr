import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk,GdkPixbuf as pixbuf

class RadioButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="RadioButton Demo")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button1 = Gtk.RadioButton.new(None)
        button1.connect("toggled", self.on_button_toggled, "1")
        button1.set_mode(False)
        pix = pixbuf.Pixbuf.new_from_file("icons/facebook.svg")
        pix1=pix.scale_simple(20,20,pixbuf.InterpType.BILINEAR)
        img = Gtk.Image.new_from_pixbuf(pix1)
        button1.set_image(img)
        button1.set_relief(Gtk.ReliefStyle.NONE)
        # button1.do_draw_indicator(False,False)
        hbox.pack_start(button1, False, False, 0)

        button2 = Gtk.RadioButton.new_from_widget(button1)
        button2.set_label("Button 2")
        button2.connect("toggled", self.on_button_toggled, "2")
        hbox.pack_start(button2, False, False, 0)

        button3 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1,
            "B_utton 3")
        button3.connect("toggled", self.on_button_toggled, "3")
        hbox.pack_start(button3, False, False, 0)

        a = button1.get_group()
        button4 = Gtk.RadioButton.new_with_label(None,"Checkbtn1")
        button4.set_mode(False)
        button4.join_group(button1)
        button4.connect("toggled", self.on_button_toggled,"CHECK")
        b=button1.get_group()
        hbox.pack_start(button4,False,False,0)

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
            Gtk.StyleContext.add_class(button.get_style_context(), "toggleasd")
        else:
            state = "off"
            Gtk.StyleContext.remove_class(button.get_style_context(),"toggleasd")
        print("Button", name, "was turned", state)

cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,Gtk.STYLE_PROVIDER_PRIORITY_USER)

win = RadioButtonWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()