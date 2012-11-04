#Filtering CS 450
#Lab 7
#Carl Wieland
import numpy as np
from numpy.fft import *
import matplotlib.pyplot as plt
import Image
from math import *
"""
A. 1-D Filtering
Design a 1-D low-pass filter to smooth the data in 1D_Noise.dat.
You may use any of the low-pass filters in Section 4.8 or design
your own. Make sure to describe your filter and its results/side
effects in your write-up.
"""
def partA():
    f = []
    dat = open("1D_Noise.dat")
    for l in dat:
        f.append(float(l))
    F = np.fft.fft(f)
    t = np.arange(len(f))
    freq = np.fft.fftfreq(t.shape[-1])
    #plot real
    plt.plot(freq,f)
    plt.title("f(u)")
    plt.show()
    G = []
    #butterworth = 1/ (1+ (u**2/ uc**2)^n)
    for x in xrange(len(f)):
        #fill up G
        G.append(1/(1+(x**2/4)))
    H = []
    for x,y in zip(F,G):
        H.append(x*y)
    h = np.fft.ifft(H)
    plt.plot(freq,h)
    plt.title("h(u) using 1/(1+ (u**2/4))")
    plt.show()

"""
B. 2-D Filtering / Convolution Theorem

Use the Convolution Theorem to implement a 9x9 
uniform spatial averaging filter in the Frequency
Domain. That is, your code should produce the same
results as you obtained in Homework #2 for spatial
filtering with a uniform-averaging 9x9 kernel, but
your implementation should use frequency-domain
filtering, not convolution. Test your implementation
using the image 2D_White_Box.pgm.

Be careful to keep in mind where the origin (center)
of the kernel/filter is. Think about what happens if
you don't position the kernel correctly.
"""
def partB():
    dat = Image.open("2D_White_Box.pgm")
    height = dat.size[1]
    width = dat.size[0]
    f = []
    kern = []
    ksize = 9
    for y in xrange(height):
        f.append([])
        kern.append([])
        for x in xrange(width):
            f[y].append(dat.getpixel((x,y)))

            if x+y <= ksize:#topleft
                kern[y].append(1)
            elif (width-1 - x)+y <=ksize:#topright
                kern[y].append(1)
            elif (x+(height-1-y)) <= ksize:#bottomleft
                kern[y].append(1)
            elif (width - 1-x)+(height-1-y) <= ksize:#bottomright
                kern[y].append(1)
            else:
                kern[y].append(0)
    F = np.fft.fft2(f)
    G = np.fft.fft2(kern)
    H = [];
    z = 0
    for x,y in zip(F,G):
        H.append([])
        for a, b in zip(x,y):
            H[z].append(a*b)
        z+=1
    h = np.fft.ifft2(H)
    out_image = Image.new('L', (width, height))
    pix_dx = out_image.load()
    for y in xrange(height):
        for x in xrange(width):
            pix_dx[x,y]=h[y][x].real
    out_image.show()
"""
C. Interference Pattern

The image interfere.pgm has an interference pattern of
unknown spatial frequency, orientation, and magnitude.
(It is, however, a single frequency.) Write a program
to automatically find and eliminate it. Remember that
you'll have to eliminate both that frequency and its
inverse frequency.


Hints:
The frequency you're looking for isn't necessarily the
one with the greatest magnitude. It's the one that is
most "out of place".
Don't just zero the frequency--having that frequency
missing can be just as bad as having too much of it.
Try to estimate a reasonable magnitude using similar frequencies.
"""
def partC():
    pass

#partA()
partB()
partC()