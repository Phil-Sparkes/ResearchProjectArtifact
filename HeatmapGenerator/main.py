import numpy as np
import matplotlib.pyplot as plt
import sqlite3
#import unittest

xValues = []
yValues = []

MAP_X_START = -7200
MAP_X_END   = 10350
MAP_Y_START = -6200
MAP_Y_END   = 10000

ENEMY_X_START = -100 # -50
ENEMY_X_END   = 100 #50
ENEMY_Y_START = 0
ENEMY_Y_END   = 200

# 1 = HitLoc
# 2 = Crouch
# 3 = XRay

ViewMap = 0
playerToCheckStart = 0
playerToCheckEnd = 0


def readTable(table):
    x = []
    y = []
    # get database
    conn = sqlite3.connect(r"data.database")
    # Get all values from database
    for row in conn.execute('SELECT * FROM ' + table):
        # Set x and y values accordingly
        if playerToCheckStart <= int(row[2]) <= playerToCheckEnd or int(row[2]) == 0 or playerToCheckStart == 0:
            x.append(float(row[0]))
            y.append(float(row[1]))
    return x, y


def checkValuesWithinMapBounds(x, y):
    for value in x:
        if value < MAP_X_START or value > MAP_X_END:
            #print 'x ' + str(value)
            return False
    for value in y:
        if value < MAP_Y_START or value > MAP_Y_END:
            #print 'y ' + str(value)
            return False
    return True

def checkValuesWithinHitboxBounds(x, y):
    counter = 0
    for value in x:
        counter += 1
        if value < ENEMY_X_START or value > ENEMY_X_END:
            #print str(counter) + ' x ' + str(value)
            return False
    for value in y:
        if value < ENEMY_Y_START or value > ENEMY_Y_END:
            #print 'y ' + str(value)
            return False
    return True

# heatmap code from https://pythonspot.com/generate-heatmap-in-matplotlib/
def generateHeatmap(x, y, binX, binY, title):
    # Create heatmap
    heatmap, yedges, xedges = np.histogram2d(y, x, bins=(binY, binX))  # bins is blocks per axis
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # Plot heatmap
    plt.clf()
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.imshow(heatmap, extent=extent, origin='lower', interpolation='bilinear')
    plt.show()
    return True


def unittest():
    assert checkValuesWithinMapBounds([1, 2, 3], [1, 2, 3]) == True
    assert checkValuesWithinMapBounds([-1, -2, -3], [-1, -2, -3]) == True
    assert checkValuesWithinMapBounds([1000, 2000, 3000], [1000, 2000, 3000]) == True
    assert checkValuesWithinMapBounds([-1000, -2000, -3000], [-1000, -2000, -3000]) == True
    assert checkValuesWithinMapBounds([-5634, -6364, -7123], [7320, 8564, 9864]) == True
    assert checkValuesWithinMapBounds([8632, 9152, 10253], [-4252, -5232, -6124]) == True

    assert checkValuesWithinMapBounds([-7231, 2, 3], [1, 2, 3]) == False
    assert checkValuesWithinMapBounds([-1, -2, -3], [-1, -2, -7203]) == False
    assert checkValuesWithinMapBounds([11000, 12000, 13000], [11000, 12000, 13000]) == False
    assert checkValuesWithinMapBounds([-11000, -12000, -13000], [-11000, -12000, -13000]) == False
    assert checkValuesWithinMapBounds([-5634, -6364, -7423], [7320, 8564, 10864]) == False
    assert checkValuesWithinMapBounds([8632, 9152, 10253], [-4252, -5232, -6424]) == False

unittest()

if ViewMap == 1:
    xValues, yValues = readTable('table_hitLocation')
    generateHeatmap(xValues, yValues, 8, 40, 'Hit Location')
elif ViewMap == 2:
    xValues, yValues = readTable('table_Crouch')
    generateHeatmap(xValues, yValues, 20, 20, 'Crouch')
elif ViewMap == 3:
    xValues, yValues = readTable('table_XRay')
    generateHeatmap(xValues, yValues, 20, 20, 'XRay')




