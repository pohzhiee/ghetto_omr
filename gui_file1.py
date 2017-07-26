import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class DialogExample(Gtk.Dialog):

    def __init__(self, parent,win_name):
        Gtk.Dialog.__init__(self, win_name, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(300, 300)

        label = Gtk.Label("This is a dialog to display additional information")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class DialogWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Dialog Example123")

        self.set_border_width(6)
        box1 = Gtk.Box(spacing=6)
        self.add(box1)

        button = Gtk.Button("Open dialog")
        button.connect("clicked", self.on_button_clicked)
        box1.pack_start(button,True,True,20)

        button2 = Gtk.Button("Open dialog22")
        button2.connect("clicked",self.on_button2_clicked)
        box1.pack_start(button2,True,True,20)

    def on_button_clicked(self, widget):
        dialog = DialogExample(self,"asdf1")
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()

    def on_button2_clicked(self, widget):
        self.dialog1 = DialogExample(self,"asdf")
        self.response1 = self.dialog1.run()

        if self.response1 == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif self.response1 == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked2")

        self.dialog1.destroy()

win = DialogWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
