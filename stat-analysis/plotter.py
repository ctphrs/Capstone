import matplotlib.pyplot as plt
import numpy as np

'''
Plots a joints behavior over time.
Takes movement_string as input
'''
def plot_joint(move_string):
    xaxis = np.linspace(1, np.size(move_string)//2, num = np.size(move_string)//2) #Divide by two because of two columns
    xdata = move_string[:,0]
    ydata = move_string[:,1]
    plt.plot(xaxis,xdata,'r-',label='X Coordinate')
    plt.plot(xaxis,ydata,'g-',label='Y Coordinate')
    plt.ylabel('Delta Position')
    plt.xlabel('Frame #')
    plt.legend()
    plt.show()
