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
            "4 : HWB\n"+
            "5 : CMY\n"+
            "6 : XYZ\n"+
            "7 : Lab\n"+
            "8 : Lch\n"+
            "9 : HCG")
    #TODO more color spaces
    cSpace = input("+>")
    img = imgName.split('.')[0]
    while ((not cSpace.isdigit()) or (int(cSpace) < 1) or (int(cSpace) > 9 )):
        print("Please enter valid number")
        cSpace = input("+>")
    if cSpace == '1':
        plot_rgb(pixels, img)
    elif cSpace == '2':
        plot_hsl(pixels, img)
    elif cSpace == '3':
        plot_hsv(pixels, img)
    elif cSpace == '4':
        plot_hwb(pixels, img)
    elif cSpace == '5':
        plot_cmy(pixels, img)
    elif cSpace == '6':
        plot_xyz(pixels, img)
    elif cSpace == '7':
        plot_lab(pixels, img)
    elif cSpace == '8':
        plot_lch(pixels, img)
    elif cSpace == '9':
        plot_hcg(pixels, img)

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
    colors = ['rgb('+str(r)+','+str(g)+','+str(b)+')' for (r,g,b) in pix]
    x,y,z = [], [], []
    for item in pix:
        R, G, B = item[0]/255, item[1]/255, item[2]/255
        Cmax = max(R, G, B)
        Cmin = min(R, G, B)
        delta = Cmax - Cmin
        L = (Cmax + Cmin)/2
        if delta == 0:
            H = 0
        elif Cmax == R:
            H = 60 * (((G - B)/delta) % 6)
        elif Cmax == G:
            H = 60 * (((B - R)/delta) + 2)
        elif Cmax == B:
            H = 60 * (((R - G)/delta) + 4)
        if delta == 0:
            S = 0
        else:
            S = delta/(1 - abs((2 * L) - 1))

        x.append(H)
        y.append(S*100)
        z.append(L*100)

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
                title= "H",
                range= [0, 360]
                ),
            yaxis=dict(
                title= "S",
                range= [0, 100]
                ),
            zaxis=dict(
                title= "L",
                range= [0, 100]
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
    py.plot(fig, filename=img+'HSL')

def plot_hsv(pix, img):
    '''
    Plots colors in HSV color space in plotly 3D Scatter plot
    '''
    colors = ['rgb('+str(r)+','+str(g)+','+str(b)+')' for (r,g,b) in pix]
    x,y,z = [], [], []
    for item in pix:
        R, G, B = item[0]/255, item[1]/255, item[2]/255
        Cmax = max(R, G, B)
        Cmin = min(R, G, B)
        delta = Cmax - Cmin
        V = Cmax
        if delta == 0:
            H = 0
        elif Cmax == R:
            H = 60 * (((G - B)/delta) % 6)
        elif Cmax == G:
            H = 60 * (((B - R)/delta) + 2)
        elif Cmax == B:
            H = 60 * (((R - G)/delta) + 4)
        if delta == 0:
            S = 0
        else:
            S = delta/Cmax

        x.append(H)
        y.append(S*100)
        z.append(V*100)

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
                title= "H",
                range= [0, 360]
                ),
            yaxis=dict(
                title= "S",
                range= [0, 100]
                ),
            zaxis=dict(
                title= "V",
                range= [0, 100]
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
    py.plot(fig, filename=img+'HSV')

def plot_hwb(pix, img):
    '''
    Plots colors in HWB color space in plotly 3D Scatter plot
    '''
    colors = ['rgb('+str(r)+','+str(g)+','+str(b)+')' for (r,g,b) in pix]
    x,y,z = [], [], []
    for item in pix:
        R, G, B = item[0]/255, item[1]/255, item[2]/255
        Cmax = max(R, G, B)
        Cmin = min(R, G, B)
        delta = Cmax - Cmin
        V = Cmax
        if delta == 0:
            H = 0
        elif Cmax == R:
            H = 60 * (((G - B)/delta) % 6)
        elif Cmax == G:
            H = 60 * (((B - R)/delta) + 2)
        elif Cmax == B:
            H = 60 * (((R - G)/delta) + 4)
        if delta == 0:
            S = 0
        else:
            S = delta/Cmax

        x.append(H)
        y.append(S*100)
        z.append(V*100)
    print("a")

def plot_cmy(pix, img):
    '''
    Plots colors in CMY color space in plotly 3D Scatter plot
    '''
    colors = ['rgb('+str(r)+','+str(g)+','+str(b)+')' for (r,g,b) in pix]
    x,y,z = [], [], []
    for item in pix:
        R, G, B = item[0], item[1], item[2]
        C, M, Y = 1 - (R/255), 1 - (G/255), 1 - (B/255)
        x.append(C*100)
        y.append(M*100)
        z.append(Y*100)

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
                title= "C",
                range= [0, 100]
                ),
            yaxis=dict(
                title= "M",
                range= [0, 100]
                ),
            zaxis=dict(
                title= "Y",
                range= [0, 100]
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
    py.plot(fig, filename=img+'CMY')

def plot_xyz(pix, img):
    print('a')

def plot_lab(pix, img):
    print('a')

def plot_lch(pix, img):
    print('a')

def plot_hcg(pix, img):
    print('a')

if __name__ == '__main__':
    '''
    Takes in photo from command line
    '''
    if len(sys.argv) < 2:
        print('Usage: py ColorPlot [imagename]')
        sys.exit()
    prompt_CS(sys.argv[1])
