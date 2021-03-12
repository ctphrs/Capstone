import matplotlib.pyplot as plt
import numpy as np

'''
Plots a joints behavior over time.
Takes string as input
'''
def plot_joint(data):
    xaxis = np.linspace(1, np.size(data)//2, num = np.size(data)//2) #Divide by two because of two columns
    xdata = data[:,0]
    ydata = data[:,1]
    plt.plot(xaxis,xdata,'r-')
    plt.plot(xaxis,ydata,'g-')
    plt.show()
