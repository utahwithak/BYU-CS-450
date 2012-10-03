import Image

"""
Sobel kerns
     -1 0 1        -1 -2 -1
dx = -2 0 2    dy = 0  0  0
     -1 0 1         1  2  1
"""
def sobel_dx(img):
	width = img.size[0]
	height = img.size[1]
	dx = [[-1,0,1],[-2,0,2],[-1,0,1]]
	#Everything is equal
	out_dx = Image.new('L', (width, height)) # Create a blank image
	pix_dx = out_dx.load()
	for y in xrange(height):
		for x in xrange(width):
			pix_dx[x,y] = 50

			num_avgs = 8
			sum_dx = 0
			
			k_y_offset = 0
			for box_y in xrange((y-1),(y+2)):
				k_x_offset=0
				for box_x in xrange((x-1),(x+2)):
					k_val_dx = dx[k_y_offset][k_x_offset]
					try:
						sum_dx = sum_dx + (img.getpixel((box_x,box_y)) * k_val_dx)
					except Exception, e:
						pass
					k_x_offset = k_x_offset+1
				k_y_offset = k_y_offset+1

			pix_dx[x,y] =pix_dx[x,y] + int(sum_dx/num_avgs)
	return out_dx

def sobel_dy(img):
	width = img.size[0]
	height = img.size[1]
	dy = [[-1,-2,-1],[0,0,0],[1,2,1]]
	out_dy = Image.new('L', (width, height)) # Create a blank image
	pix_dy = out_dy.load()
	for y in xrange(height):
		for x in xrange(width):
			pix_dy[x,y] = 50
			num_avgs = 8
			sum_dy = 0
			k_y_offset = 0
			for box_y in xrange((y-1),(y+2)):
				k_x_offset=0
				for box_x in xrange((x-1),(x+2)):
					k_val_dy = dy[k_y_offset][k_x_offset]
					try:
						sum_dy = sum_dy +(img.getpixel((box_x,box_y)) * k_val_dy)
					except Exception, e:
						pass
					k_x_offset = k_x_offset+1
				k_y_offset = k_y_offset+1
			pix_dy[x,y] =pix_dy[x,y] + int(sum_dy/num_avgs)
	return out_dy


def number1():
	"""
	1. Using the input image 2D_White_Box.pgm, separately apply the following masks and explain the results for each:
		a. Uniform averaging kernels of size 3x3, 5x5, 7x7, and 9x9. (You can reuse your code from the last assignment for this.)
		b. Each of the Sobel kernels (first derivatives in x and y respectively).
			Note: each of these should be normalized by 8.
		c.The Laplacian kernel. 
			(No normalization required mathematically, but be careful:
			 the results can be in the range [-255*4,+255*4] or larger 
			 depending on the kernel used.
	"""
	img = Image.open("2D_White_Box.pgm")
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
				for box_y in xrange((y-offset),(y+offset+1)):
					for box_x in xrange((x-offset),(x+offset+1)):
						try:
							sum = sum + img.getpixel((box_x,box_y))
						except Exception, e:
							pass
				pixels[x,y]=int(sum/num_avgs)
		out_img.save("uniformAvgK_size%i.png"%k_size)


	sobel_dy(img).save("1sobeldy.png")
	sobel_dx(img).save("1sobeldx.png")

	"""
			   0  1 0
	Laplacian: 1 -4 1
			   0  1 0
	"""

	la_kern = [[0,1,0],[1,-4,1],[0,1,0]]
	out_img = Image.new('L', (width, height)) # Create a blank image
	pixels = out_img.load()
	for y in xrange(height):
		for x in xrange(width):
			pixels[x,y] = 50
			k_y_offset = -1
			sum = 0
			offset = 1
			for box_y in xrange((y-offset),(y+offset+1)):
				k_x_offset = 0
				for box_x in xrange((x-offset),(x+offset+1)):
					try:
						sum = sum + (img.getpixel((box_x,box_y)) * la_kern[k_y_offset][k_x_offset])
					except Exception, e:
						pass
					k_x_offset= k_x_offset+1

				k_y_offset = k_y_offset+1
			pixels[x,y] = pixels[x,y]+int(sum)
	out_img.save("Laplacian.png")

"""2.Use the Sobel kernels to calculate gradient magnitude images for the input images 2D_White_Box.pgm and blocks.pgm.
"""
def number2():
	for f in ["2D_White_Box.pgm","blocks.pgm"]:
		img = Image.open(f)
		width = img.size[0]
		height = img.size[1]
		combined = Image.new('L', (width, height)) # Create a blank image
		out_dx = sobel_dx(img)
		out_dy = sobel_dy(img)
		comb = combined.load()
		for y in xrange(height):
			for x in xrange(width):
				comb[x,y] = out_dy.getpixel((x,y))+out_dx.getpixel((x,y))
		combined.show()
		combined.save("{0}combined.png".format(f[1]))


"""3.Again calculate the gradient magnitude image for the input image blocks.pgm, but blur the image first by a uniform 
kernel of size 3x3. Repeat this for blurring kernels of sizes 5x5, 7x7, and 9x9. What happens?
"""
#blur
def number3():
	img = Image.open("blocks.pgm")
	width = img.size[0]
	height = img.size[1]
	#Everything is equal
	for k_size in [3,5,7,9]:
		blurred = Image.new('L', (width, height)) # Create a blank image
		pixels = blurred.load()
		for y in xrange(height):
			for x in xrange(width):
				num_avgs = k_size*k_size
				sum = 0
				offset = ((k_size-1)/2)
				for box_y in xrange((y-offset),(y+offset+1)):
					for box_x in xrange((x-offset),(x+offset+1)):
						try:
							sum = sum + img.getpixel((box_x,box_y))
						except Exception, e:
							pass
				pixels[x,y]=int(sum/num_avgs)
		blurred.show()
		combined = Image.new('L', (width, height)) # Create a blank image
		out_dx = sobel_dx(blurred)
		out_dy = sobel_dy(blurred)
		comb = combined.load()
		for y in xrange(height):
			for x in xrange(width):
				comb[x,y] = out_dy.getpixel((x,y))+out_dx.getpixel((x,y))
		combined.show()
		combined.save("3k{0}combined.png".format(k_size))


"""4.Use unsharp masking to sharpen the blocks.pgm image. Try adjusting the sharpening strength and/or
radius of the blurring to find a combination you find effective or pleasing.
Note: Your results should be sharpened, but there should be no other side-effects (such as darkening 
or lightening of the overall image) Be careful here to clip values outside the range
[0,255] instead of inadvertently rescaling the values (losing contrast) or causing overflow/underflow.
"""

"""Unsharp mask

              0  -1  0 
unsh = 1/A * -1 A+4 -1 
              0  -1  0

"""
def unsharp(A,k):
	img = Image.open("blocks.pgm")
	width = img.size[0]
	height = img.size[1]
	unsh = []
	if k==3:
		unsh = [[ 0, -1, 0],
				[-1,A+4,-1],
				[ 0, -1, 0]]
	if k==5:
		unsh = [[ 0, 0,   -1, 0, 0],
				[ 0,-1,   -1,-1, 0],
				[-1,-1, A+12,-1,-1],
				[ 0,-1,   -1,-1, 0],
				[ 0, 0,   -1, 0, 0]]
	if k==7:
		unsh = [[ 0,  0,  0,  -1, 0, 0, 0],
			    [ 0,  0, -1,  -1,-1, 0, 0],
			    [ 0, -1, -1,  -1,-1,-1, 0],
			    [-1, -1, -1,A+24,-1,-1,-1],
			    [ 0, -1, -1,  -1,-1,-1, 0],
			    [ 0,  0, -1,  -1,-1, 0, 0],
			    [ 0,  0,  0,  -1, 0, 0, 0]]
	if k==9:
		unsh = [[0,	0,	0,	 0,	  -1,  0,  0,  0,  0],
			    [0,	0,	0,	-1,	  -1, -1,  0,  0,  0],
			    [0,	0,	-1,	-1,	  -1, -1, -1,  0,  0],
			    [0,	-1,	-1,	-1,	  -1, -1, -1, -1,  0],
			    [-1,-1,	-1,	-1,	A+40, -1, -1, -1, -1],
			    [0,	-1,	-1,	-1,	  -1, -1, -1, -1,  0],
			    [0,	0,	-1,	-1,	  -1, -1, -1,  0,  0],
			    [0,	0,	0,	-1,	  -1, -1,  0,  0,  0],
			    [0,	0,	0,	 0,	  -1,  0,  0,  0,  0]]
	out_img = Image.new('L', (width, height)) # Create a blank image
	pixels = out_img.load()
	for y in xrange(height):
		for x in xrange(width):
			k_y_offset = -1
			sum = 0
			offset = ((k-1)/2)
			for box_y in xrange((y-offset),(y+offset+1)):
				k_x_offset = 0
				for box_x in xrange((x-offset),(x+offset+1)):
					try:
						sum = sum + ((img.getpixel((box_x,box_y)) * unsh[k_y_offset][k_x_offset]))/A
					except Exception, e:
						pass
					k_x_offset= k_x_offset+1
				k_y_offset = k_y_offset+1
			pixels[x,y]=int(sum)
	out_img.show()
	out_img.save("/Users/cwieland/Projects/CS Projects/450/More Spatial Filtering/unsharpk{0}A{1}.png".format(str(k),str(A)))

def number4():
	procs = []
	for A in [1,3,5]:
		for k in [3,5,7,9]:
			unsharp(A*k,k)

number1()
number2()
number3()
number4()


