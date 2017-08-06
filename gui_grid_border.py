import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import numpy as np
#
# class filler_cont_box(Gtk.Box):
#     def __init__(self,row_num,col_num):
#         Gtk.Box.__init__(self):
#         self.str = str(row_num)+","+str(col_num)

class filler_cont(Gtk.Box):
    def __init__(self,str1,str2):
        Gtk.Box.__init__(self)
        self.str = str(str1)+","+str(str2)
        button1 = Gtk.Button()
        button1.set_label(self.str)
        button1.connect("clicked",self.btn_clicked)
        self.set_center_widget(button1)
    def btn_clicked(self,widget):
        print (self.str," was clicked")
        print ("------------")
    


class some_grid(Gtk.Grid):
    def __init__(self,r,c):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(5)
        self.set_row_spacing(5)
        n_row = r
        n_col = c
        btn_ref = np.zeros((r,c),dtype=Gtk.Box)
        for i in range(0,r):
            for j in range(0,c):
                btn_ref[i,j]=filler_cont(i,j)
                self.attach(btn_ref[i,j],j,i,1,1)





class mainwin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)



        somegrid = some_grid(15,2)
        self.add(somegrid)




cssProvider = Gtk.CssProvider()
cssProvider.load_from_path('style.css')
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
# With the others GTK_STYLE_PROVIDER_PRIORITY values get the same result
win = mainwin()
win.show_all()
Gtk.main()