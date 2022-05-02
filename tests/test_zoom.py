import matplotlib
import matplotlib.pyplot as plt
import ipywidgets as widgets

I=[0,25e-3,50e-3,75e-3,100e-3,125e-3]
U=[0,1.7,3.4,5.1,6.8,8.5]
plt.figure("Loi d'Ohm")
plt.plot(I,U,'b+-',label='U=f(I)')
plt.legend(loc=2)
plt.show()