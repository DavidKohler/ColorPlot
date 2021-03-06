#!/usr/bin/env python3
#ColorPlot.py

'''
Author: David Kohler
ColorPlot.py
'''

import os, sys
import plotly.graph_objs as go
import random, math
import plotly

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
            "7 : CIELAB")
    cSpace = input("+>")
    img = imgName.split('.')[0]
    while ((not cSpace.isdigit()) or (int(cSpace) < 1) or (int(cSpace) > 8 )):
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
    plotly.offline.plot(fig, filename=img+'RGB')

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
    plotly.offline.plot(fig, filename=img+'HSL')

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
    plotly.offline.plot(fig, filename=img+'HSV')

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
        else:
            H = 60 * (((R - G)/delta) + 4)
        if delta == 0:
            S = 0
        else:
            S = delta/Cmax
        W = (1 - S) * V
        B = 1 - V

        x.append(H)
        y.append(W*100)
        z.append(B*100)

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
        scene=dict(
            xaxis=dict(
                title= "H",
                range= [0, 360]
                ),
            yaxis=dict(
                title= "W",
                range= [0, 100]
                ),
            zaxis=dict(
                title= "B",
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
    plotly.offline.plot(fig, filename=img+'HWB')

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
    plotly.offline.plot(fig, filename=img+'CMY')

def plot_xyz(pix, img):
    '''
    Plots colors in XYZ color space in plotly 3D Scatter plot
    '''
    colors = ['rgb('+str(r)+','+str(g)+','+str(b)+')' for (r,g,b) in pix]
    x,y,z = [], [], []
    for item in pix:
        R, G, B = item[0]/255, item[1]/255, item[2]/255
        if R > 0.04045:
            R = math.pow(((R + 0.055)/ 1.055 ), 2.4)
        else:
            R = R / 12.92
        if G > 0.04045:
            G = math.pow(((G + 0.055)/ 1.055 ), 2.4)
        else:
            G = G / 12.92
        if B > 0.04045:
            B = math.pow(((B + 0.055)/ 1.055 ), 2.4)
        else:
            B = B / 12.92
        R *= 100
        G *= 100
        B *= 100

        X = (R * 0.4124) + (G * 0.3576) + (B * 0.1805)
        Y = (R * 0.2126) + (G * 0.7152) + (B * 0.0722)
        Z = (R * 0.0193) + (G * 0.1192) + (B * 0.9505)

        x.append(X)
        y.append(Y)
        z.append(Z)

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
        scene=dict(
            xaxis=dict(
                title= "X",
                range= [0, 100]
                ),
            yaxis=dict(
                title= "Y",
                range= [0, 100]
                ),
            zaxis=dict(
                title= "Z",
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
    plotly.offline.plot(fig, filename=img+'XYZ')

def plot_lab(pix, img):
    '''
    Plots colors in CIELAB color space in plotly 3D Scatter plot
    '''
    colors = ['rgb('+str(r)+','+str(g)+','+str(b)+')' for (r,g,b) in pix]
    x,y,z = [], [], []
    for item in pix:
        R, G, B = item[0]/255, item[1]/255, item[2]/255
        if R > 0.04045:
            R = math.pow(((R + 0.055)/ 1.055 ), 2.4)
        else:
            R = R / 12.92
        if G > 0.04045:
            G = math.pow(((G + 0.055)/ 1.055 ), 2.4)
        else:
            G = G / 12.92
        if B > 0.04045:
            B = math.pow(((B + 0.055)/ 1.055 ), 2.4)
        else:
            B = B / 12.92
        R *= 100
        G *= 100
        B *= 100

        X = (R * 0.4124) + (G * 0.3576) + (B * 0.1805)
        Y = (R * 0.2126) + (G * 0.7152) + (B * 0.0722)
        Z = (R * 0.0193) + (G * 0.1192) + (B * 0.9505)

        X = X / 95.047
        Y = Y / 100
        Z = Z / 108.883

        if X > 0.008856:
            fx = (math.pow(X, 1/3))
        else:
            fx = ((903.3 * X) + 16) / 116
        if Y > 0.008856:
            fy = (math.pow(Y, 1/3))
        else:
            fy = ((903.3 * Y) + 16) / 116
        if Z > 0.008856:
            fz = (math.pow(Z, 1/3))
        else:
            fz = ((903.3 * Z) + 16) / 116

        L = (116 * fy) - 16
        a = 500 * (fx - fy)
        b = 200 * (fy - fz)

        x.append(L)
        y.append(a)
        z.append(b)

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
        scene=dict(
            xaxis=dict(
                title= "L*",
                range= [0, 100]
                ),
            yaxis=dict(
                title= "a*",
                range= [-86.185, 98.254]
                ),
            zaxis=dict(
                title= "b*",
                range= [-107.863, 94.482]
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
    plotly.offline.plot(fig, filename=img+'Lab')


if __name__ == '__main__':
    '''
    Takes in photo from command line
    '''
    if len(sys.argv) < 2:
        print('Usage: py ColorPlot [imagename]')
        sys.exit()
    prompt_CS(sys.argv[1])
