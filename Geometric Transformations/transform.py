import Image 
import math
import numpy

def pgm2pil(filename):

    try:
        inFile = open(filename)

        header = None
        size = None
        maxGray = None
        data = []

        for line in inFile:
            stripped = line.strip()

            if stripped[0] == '#': 
                continue
            elif header == None: 
                if stripped != 'P2': return None
                header = stripped
            elif size == None:
                size = map(int, stripped.split())
            elif maxGray == None:
                maxGray = int(stripped)
            else:
                for item in stripped.split():
                    data.append(int(item.strip()))

        data = numpy.reshape(data, (size[1],size[0]))/float(maxGray)*255
        return numpy.flipud(data)

    except:
        pass

    return None

def imageOpenWrapper(fname):
    pgm = pgm2pil(fname)
    if pgm is not None:
        return Image.fromarray(pgm)
    return origImageOpen(fname)

origImageOpen = Image.open
Image.open = imageOpenWrapper

def bilinear_interpolation(x, y, points):
    '''Interpolate (x,y) from values associated with four points.

    The four points are a list of four triplets:  (x, y, value).
    The four points can be in any order.  They should form a rectangle.

    '''
    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')
    if x == x1 ==_x1 and y == y1 == _y1: #All same point
        return q11
    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
           ) / ((x2 - x1) * (y2 - y1) + 0.0)

"""
1)Write a program that reads in an image and magnifies it by a specified
(integer) factor using bilinear interpolation. That is, if the image you
read in is N x M, and the magnification factor is f, the resulting image 
will be N f x M f. Test your program using parrots.pgm and factors f = 2
and f = 3.
"""
def mag(img, f):
    org_size = img.size
    out_img = Image.new('L',(int(org_size[0]*f),int(org_size[1]*f)))
    pix_dat = img.load()
    out_pix = out_img.load()
    width = out_img.size[0]
    height = out_img.size[1]
    for y in range(height):
        for x in range(width):
            x0 = float(x/f)
            y0 = float(y/f)
            fx0 = math.ceil(x0)#lower x
            fy0 = math.ceil(y0)#lower y
            cx0 = math.floor(x0)#upper x
            cy0 = math.floor(y0)#upper y

            points = [(fx0,fy0,pix_dat[fx0,fy0]),(fx0,cy0,pix_dat[fx0,cy0]),(cx0,fy0,pix_dat[cx0,fy0]),(cx0,cy0,pix_dat[cx0,cy0])]
            #print points
            interp = bilinear_interpolation(x0,y0,points)
            out_pix[x,y]=interp
            #print points
    out_img.show()


"""
2)Write a program that reads in an image and reduces it by a
specified (integer) factor. That is, if the image you read in is N x M, 
and the magnification factor is f, the resulting image will be N/f x M/f
(round these if necessary). Test your program using parrots.pgm and the images
in the provided (imageTest2.pgm, imageTest3.pgm, imageTest4.pgm). Use reduction 
factors of f = 4 and f = 8. Is there anything you have to do differently from Part 
1 in order to make this work well? (Think about the sampling theorem.)
"""
def shrink(img, f):
    org_size = img.size
    out_img = Image.new('L',(int(org_size[0]/f),int(org_size[1]/f)))
    pix_dat = img.load()
    out_pix = out_img.load()
    width = out_img.size[0]
    height = out_img.size[1]
    for y in range(height):
        for x in range(width):
            x0 = float(x*f)
            y0 = float(y*f)
            fx0 = math.ceil(x0)#lower x
            fy0 = math.ceil(y0)#lower y
            cx0 = math.floor(x0)#upper x
            cy0 = math.floor(y0)#upper y

            points = [(fx0,fy0,pix_dat[fx0,fy0]),(fx0,cy0,pix_dat[fx0,cy0]),(cx0,fy0,pix_dat[cx0,fy0]),(cx0,cy0,pix_dat[cx0,cy0])]
            #print points
            interp = bilinear_interpolation(x0,y0,points)
            out_pix[x,y]=interp
            #print points
    out_img.show()


"""3)Write a program that rotates an image around its center by a specified
angle. The transformation for rotation by angle t around point (xc, yc) is

x' = (x - xc) cos t - (y - yc) sin t + xc
y' = (x - xc) sin t + (y - yc) cos t + yc

Use the backwards warping algorithm and bilinear interpolation as discussed in class. You may choose any image you wish to test and demonstrate your code.
Apply your method to the image in 15 degree increments to rotate the image by 120 degrees. Compare this to rotating directly by 120 degrees. What happens? Why?
"""
img = Image.open("parrots.pgm")

#Part 1
mag(img,2)
mag(img,3)

#part 2


shrink(img,4)
shrink(img,8)
imageTest3 = Image.open("imageTest3.pgm")
imageTest4 = Image.open("imageTest4.pgm")
imageTest2 = Image.open("imageTest2.pgm")
shrink(imageTest2,4)
shrink(imageTest2,8)

shrink(imageTest3,4)
shrink(imageTest3,8)

shrink(imageTest4,4)
shrink(imageTest4,8)
