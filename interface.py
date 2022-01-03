import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
from treatment import *
from tkinter import *
from tkinter import filedialog
from  tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('MPI Trace Analyzer')
        self['bg'] = 'white'
        self.geometry("1280x720")

        self.grid_columnconfigure(10,weight=1)
        self.operation_table = False
        self.info = False
        self.plot = False 
        self.timeline = False
        self.mpi_op_list = []
        self.pair_isw = []
        self.x = [1,2,3,4,5,6,7,8]
        self.y = [4,1,3,6,1,3,5,2]
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
            
            nb_ra = nb_rank(self.mpi_op_list)
            nb_mess = nb_message(self.mpi_op_list)
            self.pair_isw = make_pair_isw(self.mpi_op_list)
            bad_async = nb_bad_async_message(self.pair_isw)
            tt_async = total_asynchronisme(self.pair_isw)
            text = "Number of rank: " + str(nb_ra)+ "\n" +"Number of message sent: " + str(nb_mess) + "\n" + "Number of bad async message: " + str(bad_async) + "\n" + "Async total: " + str(round(tt_async,2)) + "%"

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

            self.table_scrolly = Scrollbar(self.render_table,orient='vertical')
            self.table_scrolly.pack(side=RIGHT, fill = Y)

            self.table_scrollx = Scrollbar(self.render_table,orient='horizontal')
            self.table_scrollx.pack(side=BOTTOM, fill = X)

            self.table = ttk.Treeview(self.render_table,yscrollcommand=self.table_scrolly.set,xscrollcommand=self.table_scrollx.set)
            
            self.table.pack()
            self.table_scrollx.config(command=self.table.xview)
            self.table_scrolly.config(command=self.table.yview)

            self.table['columns'] = ('Operation_Type', 'Time_before','Time_after','Bytes','Rank','Partner','Tag','Comm','Request')

            self.table.column("#0", width=0,  stretch=NO)
            self.table.column("Operation_Type", anchor=CENTER, width=120)
            self.table.column("Time_before", anchor=CENTER, width=100)
            self.table.column("Time_after", anchor=CENTER, width=100)
            self.table.column("Bytes", anchor=CENTER, width=100)
            self.table.column("Rank", anchor=CENTER, width=100)
            self.table.column("Partner", anchor=CENTER, width=100)
            self.table.column("Tag", anchor=CENTER, width=100)
            self.table.column("Comm", anchor=CENTER, width=100)
            self.table.column("Request", anchor=CENTER, width=100)

            self.table.heading("#0",text="",anchor=CENTER)
            self.table.heading("Operation_Type", text = "Operation Type", anchor=CENTER)
            self.table.heading("Time_before", text = "Time before", anchor=CENTER)
            self.table.heading("Time_after", text = "Time after", anchor=CENTER)
            self.table.heading("Bytes", text = "Bytes", anchor = CENTER)
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

    def plot_debit(self):
        print()
    def plot_coverage(self):
        print()
    def render_plot(self):
        if self.plot == False :
            self.plot = True
            self.frame_plot = Frame(self)
            self.frame_plot.pack(side=TOP,anchor=NW,padx = 2,pady = 2)
            fig = plt.figure() 
            ax1 = fig.add_subplot()
            ax1.bar(self.x,self.y) 
            canvas = FigureCanvasTkAgg(fig,master=self.frame_plot)
            canvas.draw()
            canvas.get_tk_widget().pack(side=LEFT)
            self.frame_button=Frame(self.frame_plot,padx=3)
            self.frame_button.pack(side=RIGHT ,anchor=CENTER)
        
            self.debit=Checkbutton(self.frame_button,text="Debit",command=self.plot_debit,bd=5)
            self.debit.pack(side=TOP , anchor=NW)
            self.coverage=Checkbutton(self.frame_button,text="Coverage",command=self.plot_coverage,bd=5)
            self.coverage.pack(side=TOP , anchor=NW)
        else:
            self.plot = False
            self.frame_plot.destroy()

    def render_timeline(self):
        if self.timeline == False:
            self.timeline = True
            offset = 20
            voffset = 50
            deb = self.mpi_op_list[0].t_before
            nb_ra = nb_rank(self.mpi_op_list)
            last_op = []
            last_time = self.mpi_op_list[len(self.mpi_op_list)-1].t_before

            self.frame_timeline = Frame(self,bd=5,height = 400)
            self.frame_timeline.pack(side= TOP, anchor = W, padx = 2, pady = 2,fill = X)

            self.timeline_canvas = Canvas(self.frame_timeline,scrollregion=(0,0,last_time,nb_ra*150))

            self.timeline_scrollx = Scrollbar(self.frame_timeline,orient='horizontal')
            self.timeline_scrollx.pack(side=BOTTOM, fill = BOTH)
            self.timeline_scrollx.config(command=self.timeline_canvas.xview)

            self.timeline_scrolly = Scrollbar(self.frame_timeline,orient='vertical')
            self.timeline_scrolly.pack(side=RIGHT, fill = BOTH)
            self.timeline_scrolly.config(command=self.timeline_canvas.yview)
            
            for i in range(0,nb_ra):
                last_op.append(deb)
            for elem in self.mpi_op_list:
                if elem.operation_type != 'Init':
                    elem.draw_timeline(deb,self.timeline_canvas,last_op,offset,voffset)
                    if elem.operation_type != 'Finalize':
                        last_op[elem.rank] = elem.t_after

            for i in range(1,nb_ra):
                self.timeline_canvas.create_line(0,i*130+voffset,self.winfo_width(),i*130+voffset,dash=(4,4))

            for i in range(0,nb_ra):
                self.timeline_canvas.create_text(0,70+140*i,text = str(i),anchor = 'w')
            i = 0
            step = round(last_time/20)
            while i < last_time:
                self.timeline_canvas.create_text(offset + i,5,text = str(i) + "\n|",anchor = 'n')
                i = i + step

            self.timeline_canvas.config(xscrollcommand=self.timeline_scrollx.set, yscrollcommand=self.timeline_scrolly.set,height = nb_ra * 150 + voffset )
            self.timeline_canvas.pack(fill = BOTH,side = LEFT,expand = True)

        else:
            self.timeline = False
            self.frame_timeline.destroy()


    def create_ButtonFrame(self):

        self.menu_bar = Menu(self)

        self.menu_bar.add_command(label = "Load", command=self.browseFiles)
        self.menu_render = Menu(self.menu_bar, tearoff=0)
        self.menu_render.add_command(label = "Basic Info", command=self.render_info)
        self.menu_render.add_command(label = "Table", command=self.render_operation_table)
        self.menu_render.add_command(label = "Plot" , command=self.render_plot)
        self.menu_render.add_command(label = "Timeline" , command=self.render_timeline)
        self.menu_bar.add_cascade(label="Render",menu = self.menu_render)


        self.config(menu=self.menu_bar)


window = MainWindow()
window.mainloop()