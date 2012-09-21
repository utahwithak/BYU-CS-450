import Image
import sys

if len(sys.argv) != 4:
	print "Invalid use: imgSub.py <img1-path> <img2-path> <out-path>"
	sys.exit(-1)

img1 = Image.open(sys.argv[1])
img2 = Image.open(sys.argv[2])

width = img1.size[0]
height = img2.size[1]
print str(width)+","+str(height)
outImage = Image.new('L', (width, height))
pix = outImage.load()
for y in xrange(0,height):
	for x in xrange(0,width):
		pixel1 = img1.getpixel((x,y))
		pixel2 = img2.getpixel((x,y))
 		pix[x,y]= int(pixel1)-int(pixel2)

outImage.show()
outImage.save(sys.argv[3])

Mx = 0
My = 0
mass = 0
for y in xrange(0,height):
	for x in xrange(0,width):
		if outImage.getpixel((x,y)):
			Mx += x
			My += y
			mass += 1
COM = (float(Mx)/mass , float(My)/mass)
print COM
