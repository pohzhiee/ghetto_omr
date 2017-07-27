import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gtk

class FileChooserWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="FileChooser Example")
        self.fold_str = None
        self.grid = Gtk.Grid(column_homogeneous=False,
                         column_spacing=10,
                         row_spacing=0)
        self.add(self.grid)

        button1 = Gtk.Button("Choose File")
        button1.connect("clicked", self.on_file_clicked)
        self.grid.add(button1)

        self.text_file = Gtk.Entry()
        self.grid.attach(self.text_file,1,0,4,1)

        button2 = Gtk.Button("Choose Folder")
        button2.connect("clicked", self.on_folder_clicked)
        self.grid.attach_next_to(button2,button1,Gtk.PositionType.BOTTOM,1,1)


        self.text_folder = Gtk.Entry()
        self.grid.attach(self.text_folder,1,1,4,1)

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
            self.text_file.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            str1 = "Folder selected: " + dialog.get_filename()
            print(str1)
            self.fold_str = str1
            self.text_folder.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
win = FileChooserWindow()
win.connect("delete-event", Gtk.main_quit)
win.maximize()
win.show_all()
Gtk.main()
