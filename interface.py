import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import ipywidgets as widgets
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
        self.resizable(False,False)
        self.create_button()

    def create_button(self):
        

        btn = Button(self,width=30,height=3,text="Load trace")
        btn.grid(row=1,column=1,rowspan=1,columnspan=2,sticky='ew')
        Button(self,width=15,height=3 ,text='Global info').grid(row=2,column=1)
        Button(self,width=15,height=3, text='Table ').grid(row=2,column=2)
        Button(self,width=15,height=3, text='Plot').grid(row=3,column=1)
        Button(self,width=15,height=3, text='Timeline').grid(row=3,column=2)
window = MainWindow()
window.mainloop()