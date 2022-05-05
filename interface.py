import matplotlib
import matplotlib.pyplot as plt
import ipywidgets as widgets
import numpy as np
import matplotlib.ticker
from treatment import *
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



class global_info_window(Tk):
    
    def __init__(self,mpi_op_list):
        Tk.__init__(self)
        self.mpi_op_list=mpi_op_list
        self.title('Global info')
        self.geometry('304x490')
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
        self.pair_isw = []
        self.render_info()

    def onFrameConfigure(self, event):
        self.root.configure(scrollregion=self.root.bbox("all"))
        
    def render_info(self):
        self.frame_info = Frame(self.main, bd=5)
        self.frame_info.pack(side=TOP, anchor=NW, padx=2, pady=2)
        self.pair_isw = make_pair_isw(self.mpi_op_list)
        info = gather_info(self.mpi_op_list, self.pair_isw)
        text = "GLOBAL INFO: \n\n"+"Number of process: " + str(
              info[0]) + "\n" + "Number of message sent: " + str(
              info[1]) + "\n" + "Number of MPI function: " + str(
                len(self.mpi_op_list)
                ) + "\n" + "Number of bad async message: " + str(
                    info[2]) + "\n" + "% of mpi operation " + str(round(100 - info[3], 2)) + "%\n"
            
        process_info = gather_process_info(self.mpi_op_list,info[0])
        for i in range(0,info[0]):
            text = text + "___________________________________________\n Process " +str(i)+":\n\n" + process_info[i]

        self.info_text = Label(self.frame_info, text=text)
        self.info_text.pack(side=LEFT,anchor='w')
        self.root.configure(scrollregion=self.root.bbox("all"))
        
class Table_window(Tk):
    
    def __init__(self,mpi_op_list,ratio_cy_sec):
        Tk.__init__(self)
        self.mpi_op_list=mpi_op_list
        self.title('Operation MPI table ')
        self.geometry('1344x250')
        self.ratio_cy_sec = ratio_cy_sec
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
        self.table_scrollx.config(command=self.table.xview)
        self.table_scrolly.config(command=self.table.yview)

        self.table['columns'] = ('op_type', 'Time_before', 'Time_after',
                                 'Bytes', 'Rank', 'Partner', 'Tag', 'Comm',
                                 'Request','Root','Op_Reduce','Required_level','Provided_level')

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
        self.table.column("Root", anchor=CENTER, width=100)
        self.table.column("Op_Reduce", anchor=CENTER, width=100)
        self.table.column("Required_level", anchor=CENTER, width=100)
        self.table.column("Provided_level", anchor=CENTER, width=100)
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
        self.table.heading("Root", text="Root", anchor=CENTER)
        self.table.heading("Op_Reduce", text="Op_Reduce", anchor=CENTER)
        self.table.heading("Required_level", text="Required level", anchor=CENTER)
        self.table.heading("Provided_level", text="Provided level", anchor=CENTER)

        for elem in self.mpi_op_list:
            self.table = draw_table(elem,self.table, deb, self.ratio_cy_sec)
        self.table.pack()
        self.root.configure(scrollregion=self.root.bbox("all"))
 
class Timeline_window(Tk):
    
    def __init__(self,mpi_op_list,ratio_cy_sec):
        Tk.__init__(self)
        self.mpi_op_list=mpi_op_list
        self.title('Operation MPI table ')
        self.geometry('1045x400')
        self.ratio_cy_sec = ratio_cy_sec
        self.ratio = 1
        self.percentage = 100
        self.local_ratio = 0
        self.offset = 20
        self.voffset = 50
        self.time_len = 0
        self.nb_ra = 0
        self.render_timeline()
        
    def onFrameConfigure(self, event):
        self.root.configure(scrollregion=self.root.bbox("all"))

    def render_timeline(self):
        self.time_len = self.mpi_op_list[len(self.mpi_op_list) -1]["tsc"] - self.mpi_op_list[0]["tsc"]
        self.local_ratio = self.ratio

        self.frame_timeline = Frame(self, bd=5, height=400)
        self.frame_timeline.pack(fill=BOTH,expand=True)

        self.timeline_scrollx = Scrollbar(self.frame_timeline,orient='horizontal')
        self.timeline_scrollx.pack(side=BOTTOM, fill=BOTH)

        self.timeline_scrolly = Scrollbar(self.frame_timeline,orient='vertical')
        self.timeline_scrolly.pack(side=RIGHT, fill=BOTH)

        self.timeline_canvas = Canvas(self.frame_timeline,
                                          width=1000)

        self.draw_render_timeline()

        self.scalewidget = tk.Scale(self.frame_timeline, from_=1, to=10000, length=1000,
                                    orient=tk.VERTICAL, font="Consolas 6", command=self.resize_canvas)
        self.scalewidget.set(1)
        self.scalewidget.pack(side=tk.TOP, fill=tk.Y, expand=False)

    def resize_canvas(self,percentage):
        a,b = self.timeline_scrollx.get()

        self.timeline_canvas.delete("all")
        self.percentage = float(percentage)
        self.local_ratio = self.ratio*self.percentage
        self.draw_render_timeline()
        self.marker(a,b)
        self.timeline_scrollx.set(a,b)

    def draw_render_timeline(self):
        
        deb = self.mpi_op_list[0]["tsc"]
        self.nb_ra = nb_rank(self.mpi_op_list)
        last_op = []
        last_time = self.mpi_op_list[len(self.mpi_op_list) - 1]["tsc"]

        for i in range(0, self.nb_ra):
            last_op.append(deb)
            cpt = 0
        for elem in self.mpi_op_list:
            if elem["type"] not in MPI_INIT_OP:
                draw_timeline(elem,deb, self.timeline_canvas, last_op,
                                   self.offset, self.voffset, self.local_ratio)
                cpt = cpt + 1
                if elem["type"] != 'MpiFinalize':
                    last_op[elem["current_rank"]] = tsc_after(elem)
                    
        for i in range(1, self.nb_ra):
            self.timeline_canvas.create_line(
                0,
                i * 130 + self.voffset,
                self.timeline_canvas.bbox("all")[2],
                i * 130 + self.voffset,
                dash=(4, 4))
        
        for i in range(0, self.nb_ra):
            self.timeline_canvas.create_text(0,
                                             70 + 140 * i,
                                             text=str(i),
                                             anchor='w')
        i = 0
        
        self.timeline_canvas.config(
                xscrollcommand=self.marker,
                yscrollcommand=self.timeline_scrolly.set,
                height=self.nb_ra * 150 + self.voffset,
                scrollregion=self.timeline_canvas.bbox("all"))

        self.timeline_scrollx.config(command=self.timeline_canvas.xview)
        self.timeline_scrolly.config(command=self.timeline_canvas.yview)
        self.timeline_canvas.pack(fill=BOTH, side=LEFT, expand=True)

        self.timeline_canvas.bind('<Configure>',self.resize)

    def resize(self,event):
        w,h = event.width,event.height
        self.timeline_canvas.config(width=w-50,height=h-50)

    def marker(self,x0, x1):
        self.timeline_canvas.delete("marker")
        self.timeline_scrollx.set(x0,x1)
        a,b = self.timeline_scrollx.get()
        a_len = a * (self.time_len/self.local_ratio)
        b_len = b * (self.time_len/self.local_ratio)
        len_window = b_len - a_len
        for i in range(1,3):
            self.timeline_canvas.create_text(int(self.offset + a_len+(i/3)*len_window),
                                         5,
                                         text="%3.8f" % (float((a_len+(i/3)*len_window)*(self.local_ratio))/float(self.ratio_cy_sec)) + "\n|",
                                         anchor='n')
            self.timeline_canvas.addtag_closest("marker",a_len+(i/3)*len_window,5)
      

class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.mpi_op_list=[]
        self.title('MPI Trace Analyzer')
        self['bg'] = 'white' 
        self.resizable(False,False)
        self.load=False
        self.create_button()
        self.ratio_cy_sec = 1
        

    def global_info_window(self):
        if self.load:
            win=global_info_window(self.mpi_op_list)
            win.mainloop()

    def table_window(self):
        if self.load:
            win=Table_window(self.mpi_op_list,self.ratio_cy_sec)
            win.mainloop()

    def timeline_window(self):
        if self.load:
            win=Timeline_window(self.mpi_op_list,self.ratio_cy_sec)
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
        Button(self,width=15,height=3, text='Table ',command=self.table_window).grid(row=2,column=2)
        menu_button=Menubutton(self,width=15,height=3,text='Plot',relief='raised')
        menu_button.grid(row=3,column=1,sticky=N+S+E+W)
        menu_plot=Menu(menu_button,tearoff=0) 
        menu_plot.add_command(label="Plot throughput",command=self.plot_debit)
        menu_plot.add_command(label="Plot coverage",command=self.plot_coverage)
        menu_button.config(menu=menu_plot)
        Button(self,width=15,height=3, text='Timeline',command=self.timeline_window).grid(row=3,column=2)

window = MainWindow()
window.mainloop()