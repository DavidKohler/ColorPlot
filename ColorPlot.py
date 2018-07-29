#!/usr/bin/env python3
#ColorPlot.py

'''
Author: David Kohler
ColorPlot.py
'''

import os, sys
import matplotlib.pyplot as plt
import math, random

from mpl_toolkits.mplot3d import Axes3D
from PIL import Image

def open_image(filename):
    '''
    Opens image in RGB format
    Prints size and number of pixels
    '''
    image = Image.open(filename)
    if image == None:
        print("Specified input file " + filename + " cannot be opened.")
        return Image.new("RGB", (400, 400))
    else:
        print(str(image.size) + " = " + str(len(image.getdata()))
              + " total pixels.")
        return image.convert("RGB")

def prompt_options():
    '''
    Asks User to select what they want to do
    '''
    degreeSeparation = -1
    print("Enter 1 to view single plot")
    print("Enter 2 to save multiple angles of plot")
    choice = input()
    while((choice != "1") and (choice != "2")):
        print("Please enter a valid input")
        choice = input()
    if choice == "2":
        print("Enter degree spacing for rotation of plot (btwn 1 and 360)")
        print("Ex. Enter 1 for complete 360 view, 5 for "
                +"rotations at \nevery 5 degrees, 90 for "
                +"rotations at every 90 degrees, etc.")
        degreeSeparation = int(input())
        while((degreeSeparation < 1) or (degreeSeparation > 360)):
            print("Please enter a valid input")
            degreeSeparation = int(input())
    return degreeSeparation

def get_size():
    '''
    Asks the user if they want to do a sample or the full graph
    '''
    print("Enter 1 to make plot from smaller pixel sample (faster)")
    print("Enter 2 to make plot from set of all pixels (much slower) ")
    choice = input()
    while((choice != "1") and (choice != "2")):
        print("Please enter a valid input")
        choice = input()
    if choice == "1":
        return 1
    return 2

def run(imgName):
    '''
    Creates 3D plot of colors using (r,g,b) values
    Create new directory and saves plot from series
    of different angles
    '''
    im = open_image(imgName)
    degreeSeparation = prompt_options()
    allPixels = [(r, g, b) for (r, g, b) in im.getdata()]
    sz = get_size()
    if sz == 1:
        pixels = random.sample(allPixels, 5000)
    else:
        pixels = set(allPixels)

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim(-5, 260)
    ax.set_ylim(-5, 260)
    ax.set_zlim(-5, 260)

    ax.set_xlabel('r', color='red')
    ax.set_ylabel('g', color='green')
    ax.set_zlabel('b', color='blue')

    for pixel in pixels:
        pix01 = ((pixel[0]/255), (pixel[1]/255), (pixel[2]/255))
        ax.plot([pixel[0]], [pixel[1]], [pixel[2]],
                markerfacecolor=pix01, markeredgecolor=pix01,
                marker='o', markersize=3)

    if degreeSeparation == -1:
        plt.savefig(imgName.split('.')[0]+'Plot')
        plt.show()
    else:
        directory = ('./'+(imgName.split('.')[0])+'/')
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.chdir('./'+(imgName.split('.')[0])+'/')

        for angle in range(0, 361, degreeSeparation):
            ax.view_init(30, angle)
            plt.savefig('f'+str(angle)+'deg.png')

if __name__ == '__main__':
    '''
    Takes in photo from command line
    '''
    if len(sys.argv) < 2:
        print('Usage: py ColorPlot [imagename]')
        sys.exit()
    run(sys.argv[1])
