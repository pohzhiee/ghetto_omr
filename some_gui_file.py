import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
#arbitrary stuff
class grid1(Gtk.Grid):
    def __init__(self,parent):
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


class content_grid2(Gtk.Grid):
    def __init__(self,MainGrid):
        Gtk.Grid.__init__(self)
        self.MainGrid=MainGrid

        self.imgbox = img_box(self)
        self.attach(self.imgbox,0,0,1,1)
        self.set_hexpand(True)
        self.set_valign(Gtk.Align(3))

class img_box(Gtk.Box):
    def __init__(self,contentgrid2):
        Gtk.Box.__init__(self)
        someimg=Gtk.Image.new_from_icon_name("filenew",Gtk.IconSize.MENU)
        self.add(someimg)
        # self.win_width = contentgrid2.MainGrid.window.win_width
        # self.win_height = contentgrid2.MainGrid.window.win_height
        # # wid = self.win_width*0.7
        # # hei = self.win_height*0.8
        # # print wid
        # # print hei
        # # print "-----------------------------"
        # # self.set_size_request(wid,hei)

class steps_box(Gtk.VBox):
    def __init__(self,MainGrid):
        Gtk.VBox.__init__(self)

        self.btn1=Gtk.Button()
        self.btn1.set_image(Gtk.Image.new_from_icon_name("filenew",Gtk.IconSize.DIALOG))
        self.btn1.set_name("button1")
        self.add(self.btn1)
        #
        # self.win_width = MainGrid.window.win_width
        # self.win_height = MainGrid.window.win_height
        # wid = self.win_width * 0.1
        # hei = self.win_height
        # print "requested width: ",wid
        # print "requested height: ",hei
        # print "-----------------------------"
        # self.set_size_request(wid, hei)


class MainGrid(Gtk.Grid):
    def __init__(self,window):
        Gtk.Grid.__init__(self)
        self.window = window
        self.set_column_spacing(25)

        #arbitrary initialisations for underdeveloped stuff
        self.stepsbox = steps_box(self)
        self.contentgrid = content_grid2(self)

        #end of arbitary stuff
        self.attach(self.stepsbox,0,0,1,1)
        self.attach_next_to(self.contentgrid,self.stepsbox,Gtk.PositionType.RIGHT,1,1)
        self.name = "HELLO"


class mainwin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Ghetto OMR")
        self.set_resizable(True)
        self.connect("configure-event",self.new_dim)
        self.connect("delete-event",Gtk.main_quit)

        self.win_width = 200
        self.win_height = 200

        something = Gtk.Label("SOMETHING")
        self.maximize()
        self.count =0


        self.main = MainGrid(self)
        self.add(self.main)
        #
        # self.main.destroy()
        # self.main = Gtk.Label("SOMETHING")
        # self.add(self.main)

    def new_dim(self,widget,para):
        self.win_height = para.height
        self.win_width = para.width
        # print "---------------"
        # print "window type:", widget.get_window_type()
        # print "---------------------------------------"
        # self.count = self.count+1
        # print "count: ", self.count
        # print "-------"
        self.main.stepsbox.set_size_request(0.1*self.win_width,self.win_height)
        self.main.contentgrid.imgbox.set_size_request(0.7*self.win_width,0.7*self.win_height)
        # self.destroy_widgets()
        # self.create_widgets()

    def destroy_widgets(self):
        self.main.destroy()

    def create_widgets(self):
        self.main = Gtk.Label("SOMETHING")
        self.add(self.main)




#
cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
# With the others GTK_STYLE_PROVIDER_PRIORITY values get the same result
win = mainwin()
win.show_all()
Gtk.main()








