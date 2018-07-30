#!/usr/bin/env python3
#ColorPlot.py

'''
Author: David Kohler
ColorPlot.py
'''

import os, sys
import plotly.graph_objs as go
import plotly.plotly as py
#import matplotlib.pyplot as plt
#import numpy as np
#import math
import random

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

def get_size(totalSize):
    '''
    Asks the user for number of points to plot
    '''
    print("Enter number of points to plot, between 1 and 25000")
    choice = input("+>")
    while((not choice.isdigit()) or (int(choice) < 1)
            or ((int(choice) > 25000)) or ((int(choice) >= totalSize))):
        if ((not choice.isdigit())):
            print("Please enter a number between 1 and 25000")
        elif (int(choice) >= totalSize):
            print("Cannot use number larger than size of image")
        else:
            print("Please enter a number between 1 and 25000")
        choice = input("+>")
    return int(choice)

def prompt_CS(imgName):
    '''
    Prompts user for color space to create plot in
    '''
    im = open_image(imgName)
    allPixels = [(r, g, b) for (r, g, b) in im.getdata()]
    points = get_size(len(im.getdata()))
    pixels = random.sample(allPixels, points)

    print("Please enter number for desired color space:")
    print("1 : RGB\n"+
            "2 : HSL\n"+
            "3 : HSV\n"+
            "4 : sRGB\n"+
            "5 : CMYK")
    #TODO more color spaces
    cSpace = input("+>")
    while ((not cSpace.isdigit()) or (int(cSpace) < 1) or (int(cSpace) > 5 )):
        print("Please enter valid number")
        cSpace = input("+>")
    if cSpace == '1':
        plot_rgb(pixels, imgName.split('.')[0])
    elif cSpace == '2':
        plot_hsl(pixels, imgName.split('.')[0])
    elif cSpace == '3':
        plot_hsv(pixels, imgName.split('.')[0])
    elif cSpace == '4':
        plot_srgb(pixels, imgName.split('.')[0])
    elif cSpace == '5':
        plot_cmyk(pixels, imgName.split('.')[0])

def plot_rgb(pix, img):
    '''
    Plots colors in RGB color space in plotly 3D Scatter plot
    '''
    colors = ['rgb('+str(r)+','+str(g)+','+str(b)+')' for (r,g,b) in pix]
    x,y,z = [], [], []
    for item in pix:
        x.append(item[0])
        y.append(item[1])
        z.append(item[2])

    trace0 = go.Scatter3d(
        x = x,
        y = y,
        z = z,
        mode='markers',
        marker=dict(
            size=4,
            color = colors,
            opacity=0.8
        )
    )
    data = [trace0]
    layout = go.Layout(
        title=img,
        height=550,
        width=700,
        scene=dict(
            xaxis=dict(
                title= "R",
                range= [0, 255]
                ),
            yaxis=dict(
                title= "G",
                range= [0, 255]
                ),
            zaxis=dict(
                title= "B",
                range= [0, 255]
                ),
            ),
        margin=dict(
            l=0,
            r=0,
            b=25,
            t=50
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=img+'RGB')

def plot_hsl(pix, img):
    '''
    Plots colors in HSL color space in plotly 3D Scatter plot
    '''
    print("a")

def plot_hsv(pix, img):
    '''
    Plots colors in HSV color space in plotly 3D Scatter plot
    '''
    print("a")

def plot_srgb(pix, img):
    '''
    Plots colors in sRGB color space in plotly 3D Scatter plot
    '''
    print("a")

def plot_cmyk(pix, img):
    '''
    Plots colors in CMYK color space in plotly 3D Scatter plot
    '''
    print("a")

if __name__ == '__main__':
    '''
    Takes in photo from command line
    '''
    if len(sys.argv) < 2:
        print('Usage: py ColorPlot [imagename]')
        sys.exit()
    prompt_CS(sys.argv[1])
