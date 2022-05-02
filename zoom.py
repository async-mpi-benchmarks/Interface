from tkinter import *   
import matplotlib
import matplotlib.pyplot as plt
import ipywidgets as widgets



def create():
    I=[0,25e-3,50e-3,75e-3,100e-3,125e-3]
    U=[0,1.7,3.4,5.1,6.8,8.5]
    plt.figure("Loi d'Ohm")
    plt.plot(I,U,'b+-',label='U=f(I)')
    plt.legend(loc=2)
    plt.show()




root = Tk()
root.geometry('200x100')  
btn = Button(root, text="Créer une nouvelle fenêtre", command = create)
btn.pack(pady = 10) 
root.mainloop()