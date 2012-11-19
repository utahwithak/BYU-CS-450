import Image, ImageDraw
from math import *


def genHist(img, name="default"):

    histHeight = 120            # Height of the histogram
    histWidth = 256             # Width of the histogram
    multiplerValue = 1       # The multiplier value basically increases
                                # the histogram height so that love values
                                # are easier to see, this in effect chops off
                                # the top of the histogram.
    showFstopLines = True       # True/False to hide outline
    fStopLines = 5


    # Colours to be used
    backgroundColor = (51,51,51)    # Background color
    lineColor = (102,102,102)       # Line color of fStop Markers 
    red = (255,60,60)               # Color for the red lines
    green = (51,204,51)             # Color for the green lines
    blue = (0,102,255)              # Color for the blue lines

    hist = img.histogram()
    histMax = max(hist)
    xScale = float(histWidth)/len(hist)                     # xScaling
    yScale = float((histHeight)*multiplerValue)/histMax     # yScaling 


    im = Image.new("RGBA", (histWidth, histHeight), backgroundColor)   
    draw = ImageDraw.Draw(im)


    # Draw Outline is required
    if showFstopLines:    
        xmarker = histWidth/fStopLines
        x =0
        for i in range(1,fStopLines+1):
            draw.line((x, 0, x, histHeight), fill=lineColor)
            x+=xmarker
        draw.line((histWidth-1, 0, histWidth-1, 200), fill=lineColor)
        draw.line((0, 0, 0, histHeight), fill=lineColor)


    # Draw the RGB histogram lines
    x=0; c=0;
    for i in hist:
        if int(i)==0: pass
        else:
            color = red
            if c>255: color = green
            if c>511: color = blue
            draw.line((x, histHeight, x, histHeight-(i*yScale)), fill=color)        
        if x>255: x=0
        else: x+=1
        c+=1

    # Now save and show the histogram    
    im.save("histogram{}.png".format(name))
    im.show()





"""
Programming:

Write a program that performs color histogram equalization as described in Chapter 6 of your text.
Your code should include the following components:

Read in a color image in the ppm format.
Convert the RGB image to HSI. (You may also use HSV or other similar models, but you'll need to look up the equations for these.)
Histogram equalize the intensity portion of the HSI representation of the image. (You may find your code from Homework #2 to be useful.)
Increase the saturation by a small amount. (Remember not to exceed 1.0.)
Convert the HSI image back to RGB.
Write out the color image in ppm format.
Make sure that your code does not change the hues of the image but only histogram equalizes the intensities and boosts the saturation.
(Some hue shifting may occur when certain RGB values "max out" in one of the channels, but this should be minimal.)

Test your code using the image Dune2.ppm and a couple of color images of your choice.

A few suggestions:

The equations in your text for RGB-HSI conversion are in terms of degrees. Math functions in C++ and Java are in terms of radians.
Be careful of a 0/0 error when converting pure grays to HSI--why is this?
Try seeing if you can go from RGB to HSI and back before you start trying to code and debug the equalization part.
Be careful with the types you use for the HSI or other intermediate values. Pay attention to range, quantization, overflow, etc.
In particular, look for RGB values that go out of range when you convert back from the manipulated HSI values. (This can happen when you go to HSI, manipulate it there, and convert back.) You probably want to clip these values instead of scaling the final image range.
"""
def equalize(img, name="default"):
    genHist(img,"before{}".format(name))
    img.show()
    img.save("before{}.png".format(name))
    #normalize rgb and convert to hsi
    #Converting to HSI
    hsi = []
    for y in xrange(img.size[1]):
        hsi.append([])
        for x in xrange(img.size[0]):
            pix = img.getpixel((x,y))
            tot = pix[0]+pix[1]+pix[2]
            #r,g,b
            r = float(pix[0])/tot
            g = float(pix[1])/tot
            b = float(pix[2])/tot
            #h,s,i
            h = 0
            try:
                h=acos(  (0.5* ((r-g)+(r-b))) / ((r-g)**2 + ((r-b)*(g-b)) )**.5 )
                if b>g:
                    h = 2*pi-h
            except:
                pass
            s = 1-3*min(r,g,b)
            i = float(tot)/(3*255)
            H = h*(180/pi)
            S = s*100
            I = i*255
            hsi[y].append( (H,S,I))

    #Histogram equalize the intensity portion of the HSI representation of the image.
    #generate lookups
    i_hist = [0]*256
    for y in hsi:#y = array of tuples
        for x in y:#x = one tuple
            i_hist[int(x[2])]=i_hist[int(x[2])]+1
    #print "histogram = ",i_hist
    cumulative_histogram=[i_hist[0]]
    for i in range(1,len(i_hist)):
        cumulative_histogram.append(i_hist[i]+cumulative_histogram[i-1])
    percents = []
    area = img.size[0]*img.size[1]
    for i in cumulative_histogram:
        percents.append(float(i)/area)
    lookups = []
    for i in percents:
        lookups.append(i*255)


    #Apply Convert from HSI to RGB
    out_image = Image.new("RGB",img.size,(127,127,127))
    out_pix = out_image.load()
    for u in xrange(img.size[1]):
        for v in xrange(img.size[0]):
            H = hsi[u][v][0]
            S = hsi[u][v][1]
            I = hsi[u][v][2]
            h = float(H*pi)/180
            #swappedS = S*1.1 if S!=0 else 0
            s = float(S)/100
            s = s*1.1
            swappedI = lookups[int(I)]
            i = float(swappedI)/255
            x = i * (1-s)
            y = i * (1 + ((s*cos(h))/cos(pi/3-h)))
            z = 3*i-(x+y)
            if h< (2*pi)/3:
                #print "if",(int(y*255),int(z*255),int(x*255))
                out_pix[v,u]=(int(y*255),int(z*255),int(x*255))
            elif (2*pi)/3<= h <(4*pi)/3:
                h = h-(2*pi)/3
                y = i * (1 + ((s*cos(h))/cos(pi/3-h)))#h changed
                z = 3*i-(x+y)#y changed

                #print "first elif",(int(x*255),int(y*255),int(z*255))
                out_pix[v,u]=(int(x*255),int(y*255),int(z*255))
            elif (4*pi)/3 <=h and h<2*pi:
                h = h-(4*pi)/3
                y = i * (1 + ((s*cos(h))/cos(pi/3-h)))#h changed
                z = 3*i-(x+y)#y changed
                #print "second elif",(int(z*255),int(x*255),int(y*255))
                out_pix[v,u]=(int(z*255),int(x*255),int(y*255))
            else:
                raise "Invalid HSI to RGB Conversion"
    out_image.show()
    out_image.save("after{}.png".format(name))
    genHist(out_image,"after{}".format(name))




equalize(Image.open("Dune2.ppm"),"dune2")
equalize(Image.open("IMG_0717.jpg"),"snow")
equalize(Image.open("IMG_1306.jpg"),"fence")
equalize(Image.open("IMG_1333.jpg"),"tree")
equalize(Image.open("IMG_4044.jpg"),"green")








