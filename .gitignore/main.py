import numpy as np
import matplotlib.pyplot as plt
import sqlite3

x = []
y = []

def ReadDatabase():
    # get database
    conn = sqlite3.connect(r"data.database")
    # Get all values from database
    for row in conn.execute('SELECT * FROM table_hitLocation'):
        # Set x and y values accordingly
        x.append(float(row[0]))
        y.append(float(row[1]))

# heatmap code from https://pythonspot.com/generate-heatmap-in-matplotlib/
def CreateHeatmap():
    # Create heatmap
    heatmap, yedges, xedges = np.histogram2d(y, x, bins=(40, 8))  # bins is blocks per axis
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # Plot heatmap
    plt.clf()
    plt.title('Hit Location Heatmap')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.imshow(heatmap, extent=extent, origin='lower')
    plt.show()

ReadDatabase()
CreateHeatmap()
