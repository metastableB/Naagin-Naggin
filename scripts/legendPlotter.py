#
# @author:Don Dennis (metastableB)
# legendPlotter.py
#
# Example on how to plot data with legends
import matplotlib.pyplot as plt
import pandas as pd


def legendPlot(data, columns):
    for col in columns:
        plt.plot(data[col], label=col)
    legend = plt.legend(loc='upper center', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    plt.xlabel('xth Episode')
    plt.show()


def getData(datafile):
    data = pd.read_csv(datafile)
    data['Scaled Score'] = data['Score'] / max(data['Score'])
    return data
