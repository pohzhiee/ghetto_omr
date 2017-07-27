import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class buttontest(Gtk.Button):
    def __init__(self):
        Gtk.Button.__init__(self)
        self.img = Gtk.Image.new_from_icon_name("folder",Gtk.IconSize.MENU)
        # self.img.set_from_file("icons/folder.ico")
        # self.img.pixel-size
        self.set_image(self.img)
        self.connect("clicked",self.on_file_clicked)
    def on_file_clicked(self,widget1):
        print "clicked"

class Dash(Gtk.Notebook):
    def __init__(self):
        Gtk.Notebook.__init__(self)
        self.set_reorderable=True
        self.set_hexpand=True
        self.defaultTab()
        self.tab_count=0
    def defaultTab(self):
        tab = Tab()
        cont = buttontest()
        self.append_page(cont,tab)
    def ProjTab(self,count):
        self.tab_count = self.tab_count +1
        projtabs = []
        store = Gtk.ListStore(Tab)
        b = store.append(Tab())
        content1 = buttontest()
        self.append_page(content1,projtabs[self.tab_count])


class Tab(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self,spacing=6)
        some_string = "Tab 1"
        title_label = Gtk.Label(some_string)
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_CLOSE,Gtk.IconSize.MENU)
        close_button = Gtk.Button()
        close_button.set_image(image)
        close_button.set_relief(Gtk.ReliefStyle(2))
        close_button.connect("clicked",self.close_cb)

        self.pack_start(title_label,expand=True,fill=True,padding=0)
        self.pack_end(close_button,expand=False,fill=False,padding=0)
        self.show_all()

    def close_cb(self,widget):
        print "CLOSE CLICKED"
        self.parent.tab_count=self.parent.tab_count-1
        self.destroy()

class mainWin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Tabs test")
        self.maximize()
        dashboard = Dash()
        new_tab_btn = Gtk.Button()
        new_tab_btn.img = Gtk.Image.new_from_icon_name("gtk-new",Gtk.IconSize.MENU)
        new_tab_btn.connect("clicked",dashboard.ProjTab)
        self.box = Gtk.VBox()
        self.add(self.box)

        self.box.pack_start(new_tab_btn,False,True,0)
        self.box.pack_end(dashboard,True,True,0)
        self.add(dashboard)


win = mainWin()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()