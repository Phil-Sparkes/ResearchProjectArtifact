import numpy as np
import matplotlib.pyplot as plt
import sqlite3

x = []
y = []

# 1 = HitLoc
# 2 = Crouch
# 3 = XRay

ViewMap = 1

def ReadHitLocationTable():
    # get database
    conn = sqlite3.connect(r"data.database")
    # Get all values from database
    for row in conn.execute('SELECT * FROM table_hitLocation'):
        # Set x and y values accordingly
        x.append(float(row[0]))
        y.append(float(row[1]))

def ReadCrouchTable():
    # get database
    conn = sqlite3.connect(r"data.database")
    # Get all values from database
    for row in conn.execute('SELECT * FROM table_Crouch'):
        # Set x and y values accordingly
        x.append(float(row[0]))
        y.append(float(row[1]))
        print (row)

def ReadXRayTable():
    # get database
    conn = sqlite3.connect(r"data.database")
    # Get all values from database
    for row in conn.execute('SELECT * FROM table_XRay'):
        # Set x and y values accordingly
        x.append(float(row[0]))
        y.append(float(row[1]))


# heatmap code from https://pythonspot.com/generate-heatmap-in-matplotlib/
def CreateHitLocationHeatmap():
    # Create heatmap
    heatmap, yedges, xedges = np.histogram2d(y, x, bins=(40, 8))  # bins is blocks per axis
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # Plot heatmap
    plt.clf()
    plt.title('Hit Location Heatmap')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.imshow(heatmap, extent=extent, origin='lower' , interpolation='bilinear')
    plt.show()

# heatmap code from https://pythonspot.com/generate-heatmap-in-matplotlib/
def CreateCrouchHeatmap():
    # Create heatmap
    heatmap, yedges, xedges = np.histogram2d(y, x, bins=(40, 40))  # bins is blocks per axis
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # Plot heatmap
    plt.clf()
    plt.title('Crouch Heatmap')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.imshow(heatmap, extent=extent, origin='lower' , interpolation='bilinear') # , interpolation='bilinear'
    plt.show()

# heatmap code from https://pythonspot.com/generate-heatmap-in-matplotlib/
def CreateXRayHeatmap():
    # Create heatmap
    heatmap, yedges, xedges = np.histogram2d(y, x, bins=(10, 10))  # bins is blocks per axis
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # Plot heatmap
    plt.clf()
    plt.title('XRay Heatmap')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.imshow(heatmap, extent=extent, origin='lower', interpolation='bilinear')
    plt.show()

if (ViewMap == 1):
    ReadHitLocationTable()
    CreateHitLocationHeatmap()
elif (ViewMap == 2):
    ReadCrouchTable()
    CreateCrouchHeatmap()
elif (ViewMap == 3):
    ReadXRayTable()
    CreateXRayHeatmap()




