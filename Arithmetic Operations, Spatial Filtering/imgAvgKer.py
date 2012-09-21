import Image
img = Image.open("NoisyGull.pgm")
width = img.size[0]
height = img.size[1]
#Everything is equal
for k_size in [3,5,7,9]:
	out_img = Image.new('L', (width, height)) # Create a blank image
	pixels = out_img.load()
	for y in xrange(height):
		for x in xrange(width):
			num_avgs = k_size*k_size
			sum = 0
			offset = ((k_size-1)/2)
			for box_y in xrange((y-offset),(y+offset)):
				for box_x in xrange((x-offset),(x+offset)):
					try:
						sum = sum + img.getpixel((box_x,box_y))
					except Exception, e:
						pass
			pixels[x,y]=int(sum/num_avgs)

	out_img.show()
	out_img.save("k_size%i.png"%k_size)
