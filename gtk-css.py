import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        vbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)

        self.entries = [ Gtk.Entry() for i in range(3) ]
        for e in self.entries:
            vbox.pack_start(e, True, True, 0)
            e.connect("changed", self.on_entry_changed)
            e.set_text('123')

        button=Gtk.Button(label='ok')
        vbox.pack_end(button,True,True,0)

    def on_entry_changed(self,entry):
        ctx = entry.get_style_context()
        if not entry.get_text().isdigit():
            ctx.add_class('invalid')
        else:
            ctx.remove_class('invalid')
cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,
Gtk.STYLE_PROVIDER_PRIORITY_USER) # With the others GTK_STYLE_PROVIDER_PRIORITY values get the same result.

window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()