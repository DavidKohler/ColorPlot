#!/usr/bin/env python3
#ColorPlot.py

'''
Author: David Kohler
ColorPlot.py
'''

import os
from matplotlib import cm

import sys
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from PIL import Image

def open_image(filename):
    image = Image.open(filename)
    if image == None:
        print("Specified input file " + filename + " cannot be opened.")
        return Image.new("RGB", (400, 400))
    else:
        print(str(image.size) + " = " + str(len(image.getdata()))
              + " total pixels.")
        return image.convert("RGB")

def run(imgName):
    im = open_image(imgName)
    pixels = set([(r, g, b) for (r, g, b) in im.getdata()])

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim(-5, 260)
    ax.set_ylim(-5, 260)
    ax.set_zlim(-5, 260)

    ax.set_xlabel('r', color='red')
    ax.set_ylabel('g', color='green')
    ax.set_zlabel('b', color='blue')

    for item in pixels:
        pix01 = ((item[0]/255), (item[1]/255), (item[2]/255))
        ax.plot([item[0]], [item[1]], [item[2]],
                markerfacecolor=pix01, markeredgecolor=pix01,
                marker='o', markersize=1)

    #plt.show()

    directory = ('./'+(imgName.split('.')[0])+'/')
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir('./'+(imgName.split('.')[0])+'/')

    for angle in range(0, 361, 5):
        ax.view_init(30, angle)
        plt.savefig('fig'+str(angle)+'.png')


if __name__ == '__main__':
    #Passes a picture to be run in the program
    if len(sys.argv) < 2:
        print('Usage: py ColorPlot [imagename]')
        sys.exit()
    run(sys.argv[1])
