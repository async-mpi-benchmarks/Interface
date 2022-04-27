import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker
from treatment import *
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('MPI Trace Analyzer')
        self['bg'] = 'white'
        self.geometry("1280x720")
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
        self.root.config(xscrollcommand=self.root_scrollx.set,
                         yscrollcommand=self.root_scrolly.set)
        self.main = Frame(self.root, bg="white")
        self.root.configure(scrollregion=self.root.bbox("all"))
        self.operation_table = False
        self.root.create_window((4, 4), window=self.main, anchor="nw")
        self.main.bind("<Configure>", self.onFrameConfigure)
        self.info = False
        self.plot = False
        self.timeline = False
        self.mpi_op_list = []
        self.pair_isw = []
        self.x = []
        self.y = []
        self.var_deb = IntVar()
        self.var_cov = IntVar()
        self.ratio_cy_sec = 1
        self.create_ButtonFrame()

    def onFrameConfigure(self, event):
        self.root.configure(scrollregion=self.root.bbox("all"))

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir=".",
                                              title="Select a Trace",
                                              filetypes=(("Trace File",
                                                          "*.json*"),
                                                         ("all files", "*.*")))
        if filename:
            self.mpi_op_list = json_reader(filename)
            self.ratio_cy_sec = ratio_cycle2sec(self.mpi_op_list)

    def render_info(self):
        if self.info == False:
            self.info = True
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
        else:
            self.info = False
            self.frame_info.destroy()

    def render_operation_table(self):
        if self.operation_table == False:
            self.operation_table = True
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
        else:
            self.operation_table = False
            self.render_table.destroy()

    def plot_debit(self):
        self.x = []
        self.y = []
        self.plot = False
        if self.var_cov.get():
            self.coverage.deselect()
        self.frame_plot.destroy()
        pair = make_pair_sr(self.mpi_op_list, self.ratio_cy_sec)
        for elem in pair:
            self.y.append(elem.debit / 1000000)
            self.x.append(len(self.y))
        self.render_plot()

    def plot_coverage(self):
        self.x = []
        self.y = []
        self.plot = False
        if self.var_deb.get():
            self.debit.deselect()
        self.frame_plot.destroy()
        pair = make_pair_isw(self.mpi_op_list)
        for elem in pair:
            if elem.coverage < 100:
                self.y.append(elem.coverage)
            else:
                self.y.append(100)
            self.x.append(len(self.y))
        self.render_plot()

    def render_plot(self):
        if self.plot == False:
            self.plot = True
            self.frame_plot = Frame(self.main, bg='white')
            self.frame_plot.pack(side=TOP, anchor=NW, padx=2, pady=2)
            fig = plt.figure()
            ax1 = fig.add_subplot()
            if self.var_deb.get():
                ax1.set_xlabel("Send/Isend ID")
                ax1.set_ylabel('Throughput MB/s')
            if self.var_cov.get():
                ax1.set_xlabel("ID of couple Isend/Irecv Wait")
                ax1.set_ylabel('Coverage in %')
            if (len(self.mpi_op_list) < 100):
                ax1.bar(self.x, self.y)
                locator = matplotlib.ticker.MultipleLocator(1)
            else:
                ax1.scatter(self.x, self.y, marker='.')
                locator = matplotlib.ticker.AutoLocator()

            plt.gca().xaxis.set_major_locator(locator)
            canvas = FigureCanvasTkAgg(fig, master=self.frame_plot)
            canvas.draw()
            canvas.get_tk_widget().pack(side=LEFT, fill=X)
            self.frame_button = Frame(self.frame_plot)
            self.frame_button.pack(side=RIGHT, anchor=CENTER)

            self.debit = Checkbutton(self.frame_button,
                                     text="Throughput",
                                     command=self.plot_debit,
                                     bd=5,
                                     variable=self.var_deb,
                                     highlightthickness=0)
            self.coverage = Checkbutton(self.frame_button,
                                        text="Coverage",
                                        command=self.plot_coverage,
                                        bd=5,
                                        variable=self.var_cov,
                                        highlightthickness=0)
            self.debit.pack(side=TOP, anchor=NW)
            self.coverage.pack(side=TOP, anchor=NW)

            self.root.configure(scrollregion=self.root.bbox("all"))
        else:
            self.plot = False
            self.frame_plot.destroy()

    def render_timeline(self):
        if self.timeline == False:
            self.timeline = True
            time_len = self.mpi_op_list[len(self.mpi_op_list) -1]["tsc"] - self.mpi_op_list[0]["tsc"]
            if time_len > 1000000:
                ratio = 15
            else:
                ratio = 1
            offset = 20
            voffset = 50
            deb = self.mpi_op_list[0]["tsc"]
            nb_ra = nb_rank(self.mpi_op_list)
            last_op = []
            last_time = self.mpi_op_list[len(self.mpi_op_list) - 1]["tsc"]

            self.frame_timeline = Frame(self.main, bd=5, height=400)
            self.frame_timeline.pack(side=TOP,
                                     anchor=W,
                                     padx=2,
                                     pady=2,
                                     fill=X)

            self.timeline_canvas = Canvas(self.frame_timeline,
                                          width=self.winfo_width() - 50)

            self.timeline_scrollx = Scrollbar(self.frame_timeline,
                                              orient='horizontal')
            self.timeline_scrollx.pack(side=BOTTOM, fill=BOTH)
            self.timeline_scrollx.config(command=self.timeline_canvas.xview)

            self.timeline_scrolly = Scrollbar(self.frame_timeline,
                                              orient='vertical')
            self.timeline_scrolly.pack(side=RIGHT, fill=BOTH)
            self.timeline_scrolly.config(command=self.timeline_canvas.yview)

            for i in range(0, nb_ra):
                last_op.append(deb)
            cpt = 0
            for elem in self.mpi_op_list:
                if elem["type"] != 'MpiInit' and elem["type"] != 'MpiInitThread':
                    draw_timeline(elem,deb, self.timeline_canvas, last_op,
                                       offset, voffset, ratio)
                    cpt = cpt + 1
                    if elem["type"] != 'MpiFinalize':
                        last_op[elem["current_rank"]] = tsc_after(elem)
                        
            for i in range(1, nb_ra):
                self.timeline_canvas.create_line(
                    0,
                    i * 130 + voffset,
                    self.timeline_canvas.bbox("all")[2],
                    i * 130 + voffset,
                    dash=(4, 4))

            for i in range(0, nb_ra):
                self.timeline_canvas.create_text(0,
                                                 70 + 140 * i,
                                                 text=str(i),
                                                 anchor='w')

            i = 0
            if time_len > 1000000:
                step = 1000
            else:
                step = 50
            #while i < self.timeline_canvas.bbox("all")[2]:
            #    print(str(i) + "/"+str(self.timeline_canvas.bbox("all")[2]))
            #    self.timeline_canvas.create_text(offset + i,
            #                                     5,
            #                                     text=str(i/self.ratio_cy_sec) + "\n|",
            #                                     anchor='n')
            #    i = i + step

            self.timeline_canvas.config(
                xscrollcommand=self.timeline_scrollx.set,
                yscrollcommand=self.timeline_scrolly.set,
                height=nb_ra * 150 + voffset,
                scrollregion=self.timeline_canvas.bbox("all"))
            self.timeline_canvas.pack(fill=BOTH, side=LEFT, expand=True)
            self.root.configure(scrollregion=self.root.bbox("all"))
        else:
            self.timeline = False
            self.frame_timeline.destroy()

    def create_ButtonFrame(self):

        self.menu_bar = Menu(self)

        self.menu_bar.add_command(label="Load", command=self.browseFiles)
        self.menu_render = Menu(self.menu_bar, tearoff=0)
        self.menu_render.add_command(label="Basic Info",
                                     command=self.render_info)
        self.menu_render.add_command(label="Table",
                                     command=self.render_operation_table)
        self.menu_render.add_command(label="Plot", command=self.render_plot)
        self.menu_render.add_command(label="Timeline",
                                     command=self.render_timeline)
        self.menu_bar.add_cascade(label="Render", menu=self.menu_render)

        self.config(menu=self.menu_bar)


window = MainWindow()
window.mainloop()