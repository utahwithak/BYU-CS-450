import Image
img = Image.open("NoisyGull.pgm")
width = img.size[0]
height = img.size[1]
#Everything is equal
for k_size in [3,5,7]:
	out_img = Image.new('L', (width, height)) # Create a blank image
	pixels = out_img.load()
	for y in xrange(height):
		for x in xrange(width):
			pix_vals = []
			sum = 0
			offset = ((k_size-1)/2)
			for box_y in xrange((y-offset),(y+offset)):
				for box_x in xrange((x-offset),(x+offset)):
					try:
						pix_vals.append(img.getpixel((box_x,box_y)))
					except Exception, e:
						pass
			pix_vals.sort()
			pixels[x,y]=pix_vals[int(len(pix_vals)/2)]

	out_img.show()
	out_img.save("m_size%i.png"%k_size)
