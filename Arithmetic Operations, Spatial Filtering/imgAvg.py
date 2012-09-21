import Image
import sys

start_img = Image.open("Frames/Cat0.pgm")

width = start_img.size[0]
height = start_img.size[1]
vals = [0]*height
for y in xrange(0,height):
	vals[y]=[]
	for x in xrange(0,width):
		vals[y].append(int(start_img.getpixel((x,y))))
outImage = Image.new('L', (width, height)) # Create a blank image

pix = outImage.load()
for i in xrange(1,40):
	cur_img = Image.open("Frames/Cat%i.pgm"%i)
	for y in xrange(0,height):
		for x in xrange(0,width):
			vals[y][x] += int(cur_img.getpixel((x,y)))
	if i in [1,4, 9, 19, 39] :
		for y in xrange(0,height):
			for x in xrange(0,width):
				pix[x,y] = vals[y][x]/(i+1)
		outImage.show()
		outImage.save("Frames/out%i.png"%i)
		print "saved: out%i"%i