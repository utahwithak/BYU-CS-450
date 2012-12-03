import Image
import ImageDraw
from array import array
from numpy import *

resids = []
avgs = []
out = zeros((256,256),dtype=dtype('b'))

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
def encodeImage(img,name = "default"):
    img.show()
    genHist(img,"preHist{0}".format(name))
    data = img.load()
    size = img.size
    out_imag = Image.new("L",img.size)
    pix = out_imag.load()

    for y in xrange(0,size[1]):
        for x in xrange(0,size[0]):
            #FIRST VALUE
            if x ==0 and y == 0:
                pix[x,y] = data[x,y]
            else:
                avg = computeAvg(data,x,y)
                dif = data[x,y]-avg
                if dif <0:
                    dif+=256
                pix[x,y] = dif
    genHist(out_imag,"resid{0}.png".format(name))
    #show_imag.show()
    out_imag.save("encode{0}.png".format(name));
    out_imag.save("encode{0}.pgm".format(name));

    out_imag.show()
    return out_imag



def computeAvg(data, x,y):
#get values around x,y
    sum = 0
    tot = 0;
    try:#top left
        sum += data[x-1,y-1]
        tot +=1
    except:
        pass
    try:#top
        sum += data[x,y-1]
        tot +=1
    except:
        pass
    try:#top-right
        sum += data[x+1,y-1]
        tot +=1
    except:
        pass
    try:#Left
        sum += data[x-1,y]
        tot +=1
    except:
        pass
    
    avg = sum/tot        
    return avg


def decodeImage(img, name = "default"):
    data = img.load()
    out_imag = Image.new("L",img.size)
    pix = out_imag.load()
    for y in xrange(0,img.size[1]):
        for x in xrange(0,img.size[0]):
            resid = data[x,y]
            #FIRST VALUE
            if x == 0 and y == 0:
                pix[x,y]=resid
            else:
                avg = computeAvg(pix,x,y)
                if avg + resid>255:
                    resid -= 256
                pix[x,y] = avg+resid

    out_imag.show() 

    return out_imag
    
name = "NoisyGull"
img = Image.open("{0}.pgm".format(name))
enc_img = encodeImage(img,name)
dec_img = decodeImage(enc_img,name)


name = "stuff"
img = Image.open("{0}.pgm".format(name))
enc_img = encodeImage(img,name)
dec_img = decodeImage(enc_img,name)


name = "ball"
img = Image.open("{0}.pgm".format(name))
enc_img = encodeImage(img,name)
dec_img = decodeImage(enc_img,name)

name = "parrots"
img = Image.open("{0}.pgm".format(name))
enc_img = encodeImage(img,name)
dec_img = decodeImage(enc_img,name)



name = "blocks"
img = Image.open("{0}.pgm".format(name))
enc_img = encodeImage(img,name)
dec_img = decodeImage(enc_img,name)










