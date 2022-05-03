import matplotlib
import matplotlib.pyplot as plt
import ipywidgets as widgets
import numpy as np
import matplotlib.ticker
from treatment import *
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class global_info_window(Tk):
    
    def __init__(self,mpi_op_list):
        Tk.__init__(self)
        self.mpi_op_list=mpi_op_list
        self.title('Global info')
        self.geometry('304x101')
        self.resizable(False,True)
        self.root = Canvas(self, bg='white')
        self.root.pack(side=TOP, anchor=NW, expand=True, fill=BOTH)
        self.root_scrolly = Scrollbar(self.root,
                                      orient='vertical',
                                      command=self.root.yview)
        self.root_scrolly.pack(side=RIGHT, fill=BOTH)
        self.root.config(yscrollcommand=self.root_scrolly.set)
        self.main = Frame(self.root, bg="white")
        self.root.configure(scrollregion=self.root.bbox("all"))
        self.root.create_window((4, 4), window=self.main, anchor="nw")
        self.main.bind("<Configure>", self.onFrameConfigure)
        self.render_info()

    def onFrameConfigure(self, event):
        self.root.configure(scrollregion=self.root.bbox("all"))

    def render_info(self):
        
        self.frame_info = Frame(self.main, bd=5)
        self.frame_info.pack(side=TOP, anchor=NW, padx=2, pady=2)
        self.pair_isw = make_pair_isw(self.mpi_op_list)
        info = gather_info(self.mpi_op_list, self.pair_isw)
        text = "Number of rank: " + str(
            info[0]) + "\n" + "Number of message sent: " + str(
                info[1]) + "\n" + "Number of MPI function: " + str(
                    len(self.mpi_op_list)
                ) + "\n" + "Number of bad async message: " + str(
                    info[2]) + "\n" + "% of mpi operation " + str(
                        round(100 - info[3], 2)) + "%"

        self.info_text = Label(self.frame_info, text=text)
        self.info_text.pack()
        self.root.configure(scrollregion=self.root.bbox("all"))
        
class Table_window(Tk):
    
    def __init__(self,mpi_op_list):
        Tk.__init__(self)
        self.mpi_op_list=mpi_op_list
        self.title('Operation MPI table ')
        self.geometry('950x250')
        self.ratio_cy_sec = 1
        self.root = Canvas(self, bg='white')
        self.root.pack(side=TOP, anchor=NW, expand=True, fill=BOTH)
        self.root_scrollx = Scrollbar(self.root,
                                      orient='horizontal',
                                      command=self.root.xview)
        self.root_scrollx.pack(side=BOTTOM, fill=BOTH)
        self.root_scrolly = Scrollbar(self.root,
                                      orient='vertical',
                                      command=self.root.yview)
        self.root_scrolly.pack(side=RIGHT, fill=BOTH)


        self.root.config(yscrollcommand=self.root_scrolly.set,xscrollcommand=self.root_scrollx.set)
        self.main = Frame(self.root, bg="white")
        self.root.configure(scrollregion=self.root.bbox("all"))
        self.root.create_window((4, 4), window=self.main, anchor="nw")
        self.main.bind("<Configure>", self.onFrameConfigure)
        self.render_operation_table()
        
    def onFrameConfigure(self, event):
        self.root.configure(scrollregion=self.root.bbox("all"))

    def render_operation_table(self):

        deb = self.mpi_op_list[0]["tsc"]
        self.render_table = Frame(self.main, bd=5)
        self.render_table.pack(side=TOP, anchor=W, padx=2, pady=2)
        self.table_scrolly = Scrollbar(self.render_table,
                                       orient='vertical')
        self.table_scrolly.pack(side=RIGHT, fill=Y)
        self.table_scrollx = Scrollbar(self.render_table,
                                           orient='horizontal')
        self.table_scrollx.pack(side=BOTTOM, fill=X)
        self.table = ttk.Treeview(self.render_table,
                                      yscrollcommand=self.table_scrolly.set,
                                      xscrollcommand=self.table_scrollx.set)
                                     

        self.table.pack()
        self.table_scrolly.config(command=self.table.yview)
        self.table['columns'] = ('op_type', 'Time_before', 'Time_after',
                                    'Bytes', 'Rank', 'Partner', 'Tag', 'Comm',
                                    'Request')

        self.table.column("#0", width=0, stretch=NO)
        self.table.column("op_type", anchor=CENTER, width=120)
        self.table.column("Time_before", anchor=CENTER, width=100)
        self.table.column("Time_after", anchor=CENTER, width=100)
        self.table.column("Bytes", anchor=CENTER, width=100)
        self.table.column("Rank", anchor=CENTER, width=100)
        self.table.column("Partner", anchor=CENTER, width=100)
        self.table.column("Tag", anchor=CENTER, width=100)
        self.table.column("Comm", anchor=CENTER, width=100)
        self.table.column("Request", anchor=CENTER, width=100)
        self.table.heading("#0", text="", anchor=CENTER)
        self.table.heading("op_type", text="Operation Type", anchor=CENTER)
        self.table.heading("Time_before",
                            text="Time before",
                            anchor=CENTER)
        self.table.heading("Time_after", text="Time after", anchor=CENTER)
        self.table.heading("Bytes", text="Bytes", anchor=CENTER)
        self.table.heading("Rank", text="Rank", anchor=CENTER)
        self.table.heading("Partner", text="Partner", anchor=CENTER)
        self.table.heading("Tag", text="Tag", anchor=CENTER)
        self.table.heading("Comm", text="Comm", anchor=CENTER)
        self.table.heading("Request", text="Request", anchor=CENTER)

        for elem in self.mpi_op_list:
            self.table = draw_table(elem,self.table, deb, self.ratio_cy_sec)
            self.table.pack()
            self.root.configure(scrollregion=self.root.bbox("all"))
 
class Timeline_window(Tk):
    
    def __init__(self,mpi_op_list):
        Tk.__init__(self)
        self.mpi_op_list=mpi_op_list
        self.title('Operation MPI table ')
        self.geometry('950x250')
        self.ratio_cy_sec = 1
        self.root = Canvas(self, bg='white')
        self.root.pack(side=TOP, anchor=NW, expand=True, fill=BOTH)
        self.root_scrollx = Scrollbar(self.root,
                                      orient='horizontal',
                                      command=self.root.xview)
        self.root_scrollx.pack(side=BOTTOM, fill=BOTH)
        self.root_scrolly = Scrollbar(self.root,
                                      orient='vertical',
                                      command=self.root.yview)
        self.root_scrolly.pack(side=RIGHT, fill=BOTH)


        self.root.config(yscrollcommand=self.root_scrolly.set,xscrollcommand=self.root_scrollx.set)
        self.main = Frame(self.root, bg="white")
        self.root.configure(scrollregion=self.root.bbox("all"))
        self.root.create_window((4, 4), window=self.main, anchor="nw")
        self.main.bind("<Configure>", self.onFrameConfigure)
        self.render_operation_table()
        
    def onFrameConfigure(self, event):
        self.root.configure(scrollregion=self.root.bbox("all"))

    def render_operation_table(self):

        deb = self.mpi_op_list[0]["tsc"]
        self.render_table = Frame(self.main, bd=5)
        self.render_table.pack(side=TOP, anchor=W, padx=2, pady=2)
        self.table_scrolly = Scrollbar(self.render_table,
                                       orient='vertical')
        self.table_scrolly.pack(side=RIGHT, fill=Y)
        self.table_scrollx = Scrollbar(self.render_table,
                                           orient='horizontal')
        self.table_scrollx.pack(side=BOTTOM, fill=X)
        self.table = ttk.Treeview(self.render_table,
                                      yscrollcommand=self.table_scrolly.set,
                                      xscrollcommand=self.table_scrollx.set)
                                     

        self.table.pack()
        self.table_scrolly.config(command=self.table.yview)
        self.table['columns'] = ('op_type', 'Time_before', 'Time_after',
                                    'Bytes', 'Rank', 'Partner', 'Tag', 'Comm',
                                    'Request')

        self.table.column("#0", width=0, stretch=NO)
        self.table.column("op_type", anchor=CENTER, width=120)
        self.table.column("Time_before", anchor=CENTER, width=100)
        self.table.column("Time_after", anchor=CENTER, width=100)
        self.table.column("Bytes", anchor=CENTER, width=100)
        self.table.column("Rank", anchor=CENTER, width=100)
        self.table.column("Partner", anchor=CENTER, width=100)
        self.table.column("Tag", anchor=CENTER, width=100)
        self.table.column("Comm", anchor=CENTER, width=100)
        self.table.column("Request", anchor=CENTER, width=100)
        self.table.heading("#0", text="", anchor=CENTER)
        self.table.heading("op_type", text="Operation Type", anchor=CENTER)
        self.table.heading("Time_before",
                            text="Time before",
                            anchor=CENTER)
        self.table.heading("Time_after", text="Time after", anchor=CENTER)
        self.table.heading("Bytes", text="Bytes", anchor=CENTER)
        self.table.heading("Rank", text="Rank", anchor=CENTER)
        self.table.heading("Partner", text="Partner", anchor=CENTER)
        self.table.heading("Tag", text="Tag", anchor=CENTER)
        self.table.heading("Comm", text="Comm", anchor=CENTER)
        self.table.heading("Request", text="Request", anchor=CENTER)

        for elem in self.mpi_op_list:
            self.table = draw_table(elem,self.table, deb, self.ratio_cy_sec)
            self.table.pack()
            self.root.configure(scrollregion=self.root.bbox("all"))


class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.mpi_op_list=[]
        self.title('MPI Trace Analyzer')
        self['bg'] = 'white' 
        self.resizable(False,False)
        self.load=False
        self.create_button()
        

    def global_info_window(self):
        if self.load:
            win=global_info_window(self.mpi_op_list)
            win.mainloop()

    def Table_window(self):
        if self.load:
            win=Table_window(self.mpi_op_list)
            win.mainloop()


    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir=".",
                                              title="Select a Trace",
                                              filetypes=(("Trace File",
                                                          "*.json*"),
                                                         ("all files", "*.*")))
        if filename:
            self.mpi_op_list = json_reader(filename)
            self.ratio_cy_sec = ratio_cycle2sec(self.mpi_op_list)
            self.load=True
        

    def plot_coverage(self):
        if self.load:
            self.x = []
            self.y = []
            pair = make_pair_isw(self.mpi_op_list)
            for elem in pair:
                if elem.coverage < 100:
                    self.y.append(elem.coverage)
                else:
                    self.y.append(100)
                self.x.append(len(self.y))
            fig = plt.figure("Coverage's diagram")
            ax1 = fig.add_subplot()
            ax1.set_xlabel("ID of couple Isend/Irecv Wait")
            ax1.set_ylabel('Coverage in %')
            if (len(self.mpi_op_list) < 100):
                ax1.bar(self.x, self.y)
                locator = matplotlib.ticker.MultipleLocator(1)
            else:
                ax1.scatter(self.x, self.y, marker='.')
                locator = matplotlib.ticker.AutoLocator()

            plt.gca().xaxis.set_major_locator(locator)
            plt.show()

    def plot_debit(self):
        if self.load:
            self.x = []
            self.y = []
            pair = make_pair_sr(self.mpi_op_list, self.ratio_cy_sec)
            for elem in pair:
                self.y.append(elem.debit / 1000000)
                self.x.append(len(self.y))
            fig = plt.figure("Throughput's diagram")
            ax1 = fig.add_subplot()
            ax1.set_xlabel("Send/Isend ID")
            ax1.set_ylabel('Throughput MB/s')
            if (len(self.mpi_op_list) < 100):
                ax1.bar(self.x, self.y)
                locator = matplotlib.ticker.MultipleLocator(1)
            else:
                ax1.scatter(self.x, self.y, marker='.')
                locator = matplotlib.ticker.AutoLocator()
            plt.gca().xaxis.set_major_locator(locator)
            plt.show()


    def create_button(self):
        btn = Button(self,width=30,height=3,text="Load trace", command=self.browseFiles)
        btn.grid(row=1,column=1,rowspan=1,columnspan=2,sticky='ew')
        Button(self,width=15,height=3 ,text='Global info',command=self.global_info_window).grid(row=2,column=1)
        Button(self,width=15,height=3, text='Table ',command=self.Table_window).grid(row=2,column=2)
        Button(self,width=15,height=3, text='Plot',command=self.plot_debit).grid(row=3,column=1)
        Button(self,width=15,height=3, text='Timeline').grid(row=3,column=2)



    

window = MainWindow()
window.mainloop()