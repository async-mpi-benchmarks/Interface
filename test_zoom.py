import matplotlib
import matplotlib.pyplot as plt
import ipywidgets as widgets

I=[0,25e-3,50e-3,75e-3,100e-3,125e-3]
U=[0,1.7,3.4,5.1,6.8,8.5]
plt.figure("Loi d'Ohm")
plt.plot(I,U,'b+-',label='U=f(I)')
plt.legend(loc=2)
plt.show()


from tkinter import *   
#Fonction
def changeText(str):  
    btn['text'] = str
gui = Tk()  
gui.geometry('200x100')  
#Bouton
btn = Button(
  gui, 
  text = "Cliquez ici!", 
  command = lambda: changeText('Welcome to WayToLearnX!')
)
btn.pack()
gui.mainloop()



import tkinter as tk
 
IMAGE_FILE_TK = 'free.png' ## À MODIFIER
 
fenetre = tk.Tk()
 
canva = tk.Canvas(fenetre)
canva.pack()
 
image = tk.PhotoImage(file=IMAGE_FILE_TK)
image = image.zoom(2) ## CHOIX 1
#image = image.zoom(1, 2) ## CHOIX 2
 
canva.create_image(10, 10, anchor='nw', image=image)
         
fenetre.mainloop()