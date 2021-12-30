from treatment import *
from tkinter import *
from tkinter import filedialog
from  tkinter import ttk

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('MPI Trace Analyzer')
        self['bg'] = 'white'
        self.geometry("1280x720")
        self.grid_columnconfigure(10,weight=1)
        self.operation_table = False
        self.info = False
        self.mpi_op_list = []
        self.pair_isw = []
        self.create_ButtonFrame()

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir = ".", title = "Select a Trace", filetypes = (("Trace File","*.json*"),("all files","*.*")))
        if filename:
            self.mpi_op_list = json_reader(filename)
            self.mpi_op_list = sorted(self.mpi_op_list,key=lambda x: x.t_before)

    def render_info(self):
        if self.info == False:
            self.info = True
            self.frame_info = Frame(self,bd = 5)
            self.frame_info.pack(side=TOP,anchor=NW,padx = 2,pady = 2)
            
            nb_mess = nb_message(self.mpi_op_list)
            self.pair_isw = make_pair_isw(self.mpi_op_list)
            bad_async = nb_bad_async_message(self.pair_isw)
            tt_async = total_asynchronisme(self.pair_isw)
            text = "Number of message sent: " + str(nb_mess) + "\n" + "Number of bad async message: " + str(bad_async) + "\n" + "Async total: " + str(round(tt_async,2)) + "%"

            self.info_text = Label(self.frame_info,text=text)
            self.info_text.pack()

        else:
            self.info = False
            self.frame_info.destroy()

    def render_operation_table(self):
        if self.operation_table == False:
            self.operation_table = True
            self.render_table = Frame(self,bd = 5)
            self.render_table.pack(side=TOP,anchor=W,padx = 2,pady = 2)

            self.table_scroll = Scrollbar(self.render_table,orient='vertical')
            self.table_scroll.pack(side=RIGHT, fill = Y)

            self.table = ttk.Treeview(self.render_table,yscrollcommand=self.table_scroll.set)
            self.table.pack()

            self.table_scroll.config(command=self.table.xview)
            self.table_scroll.config(command=self.table.yview)

            self.table['columns'] = ('Operation_Type', 'Time_before','Time_after','Rank','Partner','Tag','Comm','Request')

            self.table.column("#0", width=0,  stretch=NO)
            self.table.column("Operation_Type", anchor=CENTER, width=120)
            self.table.column("Time_before", anchor=CENTER, width=100)
            self.table.column("Time_after", anchor=CENTER, width=100)
            self.table.column("Rank", anchor=CENTER, width=100)
            self.table.column("Partner", anchor=CENTER, width=100)
            self.table.column("Tag", anchor=CENTER, width=100)
            self.table.column("Comm", anchor=CENTER, width=100)
            self.table.column("Request", anchor=CENTER, width=100)

            self.table.heading("#0",text="",anchor=CENTER)
            self.table.heading("Operation_Type", text = "Operation Type", anchor=CENTER)
            self.table.heading("Time_before", text = "Time before", anchor=CENTER)
            self.table.heading("Time_after", text = "Time after", anchor=CENTER)
            self.table.heading("Rank", text = "Rank", anchor=CENTER)
            self.table.heading("Partner", text = "Partner", anchor=CENTER)
            self.table.heading("Tag", text = "Tag", anchor=CENTER)
            self.table.heading("Comm", text = "Comm", anchor=CENTER)
            self.table.heading("Request", text = "Request", anchor=CENTER)

            for elem in self.mpi_op_list:
                self.table=elem.table(self.table)

            self.table.pack()
        else:
            self.operation_table = False
            self.render_table.destroy()

    def create_ButtonFrame(self):
        self.menu_bar = Menu(self)

        self.menu_bar.add_command(label = "Load", command=self.browseFiles)
        
        self.menu_render = Menu(self.menu_bar, tearoff=0)
        self.menu_render.add_command(label = "Basic Info", command=self.render_info)
        self.menu_render.add_command(label = "Table", command=self.render_operation_table)
        
        self.menu_bar.add_cascade(label="Render",menu = self.menu_render)

        self.config(menu=self.menu_bar)


window = MainWindow()
window.mainloop()