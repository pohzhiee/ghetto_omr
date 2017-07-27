import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class grid1(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self,column_homogeneous=False, column_spacing=10,row_spacing=0)
        button1 = Gtk.Button("Choose File")
        button1.connect("clicked", self.on_file_clicked)
        self.add(button1)

        self.text_file = Gtk.Entry()
        self.text_file.set_hexpand(True)
        self.attach(self.text_file, 1, 0, 4, 1)

        button2 = Gtk.Button("Choose Folder")
        button2.connect("clicked", self.on_folder_clicked)
        self.attach_next_to(button2, button1, Gtk.PositionType.BOTTOM, 1, 1)

        self.text_folder = Gtk.Entry()
        self.attach(self.text_folder, 1, 1, 4, 1)
    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.get_toplevel(),
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
        dialog = Gtk.FileChooserDialog("Please choose a folder", self.get_toplevel(),
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


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Simple Notebook Example")
        self.set_border_width(8)
        self.maximize()

        self.notebook = Gtk.Notebook()


        self.some_button = Gtk.Button("NEW TAB")
        self.some_button.connect("clicked",self.new_tab)


        self.main_grid = Gtk.Grid(row_homogeneous = False, column_spacing =0, row_spacing =10)


        self.add(self.main_grid)

        self.main_grid.add(self.some_button)
        self.main_grid.attach(self.notebook,0,1,1,1)
        self.notebook.set_hexpand(True)

        # self.add(self.some_button)
        # self.add(self.notebook)

        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label('Default Page!'))
        self.notebook.append_page(self.page1, Gtk.Label('Plain Title'))

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label('A page with an image for a Title.'))
        self.notebook.append_page(
            self.page2,
            Gtk.Image.new_from_icon_name(
                "help-about",
                Gtk.IconSize.MENU
            )
        )
        self.page3 = grid1()
        self.page3.set_border_width(10)
        self.notebook.append_page(self.page3,Gtk.Image.new_from_icon_name("security-medium",Gtk.IconSize.MENU))
    def new_tab(self,widget):
        print "new_tab"

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
