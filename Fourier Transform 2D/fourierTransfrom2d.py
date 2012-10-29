import numpy.fft
import numpy as np
import Image
from math import *
from decimal import *
import matplotlib.pyplot as plt
"""
A. Simple sines and cosines

Make a two-dimensional image that is a sinusoid in
one direction and constant in the other:

f[x,y] = sin(2 pi s x / N)
 
(Don't let the fact that the equation uses only x and not y throw you--this just means that each row (y) is the same.)

Use N = 256 and various values of s. Display each image and the magnitude of their respective Fourier Transforms.

Create another two-dimensional image, again with a sinusoid in one direction and constant in the other, only swap
the two directions: f[x,y] = sin(2 pi s y / N). Again use N = 256 but choose a different value for the frequency
than that used in Part A. Again display the image and the magnitude of its Fourier Transform.
"""
def partA():
	s = 2
	f = []
	for y in xrange(256):
		f.append([])
		value = sin((2*pi*s*y)/256)
		for x in xrange(256):
			f[y].append(value)
	sp = np.fft.fft2(f)

	out_image = Image.new('L', (256, 256))

	mag_image = Image.new('L', (256, 256))
	pix_dx = out_image.load()
	pix_mag = mag_image.load()
	for y in xrange(256):
		for x in xrange(256):
			pix_dx[x,y] = (f[y][x]*127)+127
			mag = sqrt(sp[y][x].real**2+sp[y][x].imag**2)
			pix_mag[x,y] = (mag*127)+127
	out_image.show()
	out_image.save("parta.png")
	mag_image.show()
	mag_image.save("F partaa.png")

	"""
		Switch Axis
	"""
	s = 10
	f = []

	for y in xrange(0,256):
		f.append([])
		for x in xrange(0,256):
			f[y].append(sin((2*pi*s*x)/256))
	sp = np.fft.fft2(f)

	out_image = Image.new('L', (256, 256))

	mag_image = Image.new('L', (256, 256))
	pix_dx = out_image.load()
	pix_mag = mag_image.load()
	for y in xrange(256):
		for x in xrange(256):
			pix_dx[x,y] = (f[y][x]*127)+127
			mag = sqrt(sp[y][x].real**2+sp[y][x].imag**2)
			pix_mag[x,y] = (mag*127)+127
	out_image.show()
	out_image.save("swapped f of part ab.png")
	mag_image.show()
	mag_image.save("F of partab.png")


"""
B. Addition

Add the two images from Part A together.
Display the magnitude part of the Fourier Transform of the sum and explain.

"""
def partB():
	dx = []
	dy = []
	f = []
	for y in xrange(256):
		dx.append([])
		dy.append([])
		for x in xrange(256):
			dx[y].append( sin((2*pi*2*x)/256) )
			dy[y].append( sin((2*pi*4*y)/256) )

	for y in xrange(256):
		f.append([])
		for x in xrange(256):
			f[y].append(dx[y][x]+dy[y][x])
	sp = np.fft.fft2(f)
	mag_image = Image.new('L', (256, 256))
	pix_mag = mag_image.load()
	for y in xrange(256):
		for x in xrange(256):
			mag = sqrt(sp[y][x].real**2+sp[y][x].imag**2)
			pix_mag[x,y] = (mag*127)+127
	mag_image.show()
	mag_image.save("F of partb.png")



"""
C. Rotation

Using the image created in Part B that is the sum of a sinusoid in one direction and a sinusoid in the other,
rotate the image (use Photoshop, GIMP, or comparable tools) and display the result.
Display the magnitude part of the Fourier Transform of the rotated image and explain.
"""
def partC():
	mag_image = Image.new('L', (256, 256))
	pix_mag = mag_image.load()
	for y in xrange(256):
		for x in xrange(256):
			pix_mag[y,x] =( sin((2*pi*2*x)/256)*127)+127
	mag_image.show()
	mag_image=mag_image.rotate(45)

	mag_image.show()
	mag_image.save("partC.png")
	f = []
	for y in xrange(256):
		f.append([])
		for x in xrange(256):
			f[y].append(mag_image.getpixel((y,x)))
	sp = np.fft.fft2(f)
	mag_image = Image.new('L', (256, 256))
	pix_mag = mag_image.load()
	for y in xrange(256):
		for x in xrange(256):
			mag = sqrt(sp[y][x].real**2+sp[y][x].imag**2)
			pix_mag[x,y] = (mag*127)+127
	mag_image.show()
	mag_image.save("F of partC.png")
"""
D. Multiplication

Do the same thing as in Part B, except multiply the two images instead of adding them.
Explain why you get this result.
"""
def partD():

	dx = []
	dy = []
	f = []
	for y in xrange(256):
		dx.append([])
		dy.append([])
		for x in xrange(256):
			dx[y].append( sin((2*pi*2*x)/256) )
			dy[y].append( sin((2*pi*4*y)/256) )

	for y in xrange(256):
		f.append([])
		for x in xrange(256):
			f[y].append(dx[y][x]*dy[y][x])
	

	sp = np.fft.fft2(f)


	mag_image = Image.new('L', (256, 256))
	pix_mag = mag_image.load()
	for y in xrange(256):
		for x in xrange(256):
			mag = sqrt(sp[y][x].real**2+sp[y][x].imag**2)
			pix_mag[x,y] = (mag*127)+127
	mag_image.show()
	mag_image.save("F of partD.png")



"""
E. Magnitude and Phase

Using the "ball.pgm" and "gull.pgm" images,

Compute the Fourier Transform of each image.
Extract the magnitude and phase parts of each.
Pair the magnitude of one image with the phase of the other and vice versa.
Invert both (magnitude,phase) pairs and display the results.
The images you see now have the magnitude from one image and the
phase from the other. Which of the two inputs does each most look like?
"""
def partE():
	gull = Image.open("gull.pgm")
	ball = Image.open("ball.pgm")
	width = gull.size[0]
	height = gull.size[1]

	u = []
	v = []

	#phase info
	u_phase = []
	v_phase = []
	#mag infor
	u_mag = []
	v_mag =[]

	for y in xrange(height):
		u.append([])
		v.append([])
		for x in xrange(width):
			u[y].append(gull.getpixel((y,x)))
			v[y].append(ball.getpixel((y,x)))

	#fft the original images to swap into frequency domain
	f_of_u = np.fft.fft2(u)
	f_of_v = np.fft.fft2(v) 

	#containers for the mixed outputs
	mixed_u = []
	mixed_v = []
	#swap everything around
	for y in xrange(height):
		u_phase.append([])
		u_mag.append([])
		v_phase.append([])
		v_mag.append([])
		mixed_u.append([])
		mixed_v.append([])
		for x in xrange(width):
			u_phase[y].append(atan2(f_of_u[y][x].imag,f_of_u[y][x].real))
			u_mag[y].append( sqrt(f_of_u[y][x].real**2+f_of_u[y][x].imag**2))

			v_phase[y].append( atan2(f_of_v[y][x].imag, f_of_v[y][x].real))
			v_mag[y].append( sqrt(f_of_v[y][x].real**2+f_of_v[y][x].imag**2))
			#real part is mag*cos(phase)
			#imaginary is mag*sin(phase)
			mixed_u[y].append( complex(u_mag[y][x]*cos(v_phase[y][x]), u_mag[y][x]*sin(v_phase[y][x])))
			mixed_v[y].append( complex(v_mag[y][x]*cos(u_phase[y][x]), v_mag[y][x]*sin(u_phase[y][x])))
	
	#inverse fft the mixed to take it back into time domain
	final_u = np.fft.ifft2(mixed_u)
	final_v = np.fft.ifft2(mixed_v)

	#create images with the inverted signals
	u_image = Image.new('L', (height, width))
	u_pix = u_image.load()

	v_image = Image.new('L', (height, width))
	v_pix = v_image.load()
	
	for y in xrange(height):
		for x in xrange(width):
			u_pix[x,y]=final_u[x][y].real
			v_pix[x,y]=final_v[x][y].real
	u_image.show()
	u_image.save("mixedGull.png")
	v_image.show()
	v_image.save("mixedBall.png")
partA()
partB()
partC()
partD()
partE()









