import numpy.fft
import numpy as np
from math import *
from decimal import *
import matplotlib.pyplot as plt
import heapq

def part1(funct, name, power=False):
	N=128
	t = np.arange(N)
	sp = np.fft.fft(funct)
	freq = np.fft.fftfreq(t.shape[-1])
	#plot real
	plt.plot(freq, sp.real)
	plt.title("Real Values {0}".format(name))
	plt.show()
	#plot imaginary
	plt.plot(freq, sp.imag)
	plt.title("Imaginary Values {0}".format(name))
	plt.show()
	#calculate magnitude
	magnitude = []
	for x,y in zip(sp.real,sp.imag):
		magnitude.append(sqrt(x**2+y**2))
	#plot magnitude
	plt.plot(freq, magnitude)
	plt.title("Magnitude {0}".format(name))
	plt.show()

	#calculate phase
	phase = []
	for x,y in zip(sp.real,sp.imag):
		if sqrt(x**2+y**2) <.00001:
			phase.append(0)
		else:
			phase.append(atan2(y,x))
	plt.plot(freq, phase)
	plt.title("Phase {0}".format(name))
	plt.show()
	if power:
		magnitude = []
		for x,y in zip(sp.real,sp.imag):
			magnitude.append(x**2+y**2)
		#plot magnitude
		plt.plot(freq, magnitude)
		plt.title("Power Function {0}".format(name))
		plt.show()



def part2():
	#read in file
	dataFile = open("/Users/cwieland/Projects/CS Projects/450/Fourier Transform/1D_Rect128.dat","r");
	data = []
	for line in dataFile:
		data.append(float(line.strip()))
	part1(data,"Rect",True)


def part3():
	#read in file
	dataFile = open("/Users/cwieland/Projects/CS Projects/450/Fourier Transform/1D_Gauss128.dat","r");
	data = []
	for line in dataFile:
		data.append(float(line.strip()))
	part1(data,"Gauss",True)

"""
D. Frequency Analysis:

Write a program that uses the Fourier Transform to identify the n most significant frequencies in a signal
(other than the constant component). Your program should read in the signal as input and print out the
dominant frequencies as output. Hint: remember that a particular frequency will be echoed in both the
positive and negative frequencies of the Fourier Transform, so be careful not to inadvertently report
the same frequency twice.

Test your program to find the three most significant frequencies in the 1-D signal found in "1D_Signal").
You should also plot this signal to see what it looks like in the time domain, but you don't need to
include this plot in your write-up.

"""
def part4():

	#read in file
	dataFile = open("/Users/cwieland/Projects/CS Projects/450/Fourier Transform/1D_Signal.dat","r");
	data = []
	for line in dataFile:
		data.append(float(line.strip()))

	t = np.arange(len(data))
	sp = np.fft.fft(data)
	freqs = np.fft.fftfreq(t.shape[-1])
	absVal = []
	for val in freqs:
		if abs(val) not in absVal:
			absVal.append(abs(val))

	#plot real
	plt.plot(freqs, data)
	plt.title("Real Values {0}".format("Signal"))
	plt.show()

	maxes = heapq.nlargest(3, absVal)
	print maxes
	

def part5():
	dataFile = open("/Users/cwieland/Projects/CS Projects/450/Fourier Transform/1D_Rect128.dat","r");
	inputVals = []
	for line in dataFile:
		inputVals.append(float(line.strip()))
	fOfU = np.fft.fft(inputVals)
	
	dataFile = open("/Users/cwieland/Projects/CS Projects/450/Fourier Transform/1D_Output128.dat","r");
	outVals = []
	for line in dataFile:
		outVals.append(float(line.strip()))
	gOfU = np.fft.fft(outVals)


	hOfU = []
	reals = []
	for x, xi, y, yi in zip(fOfU.real,fOfU.imag,gOfU.real,gOfU.imag):
		if x < .001:
			hOfU.append(0)
			reals.append(0)
		else:
			val = complex(y,yi)/complex(x,xi)
			hOfU.append(val)
			reals.append(val.real)

	t = np.arange(len(hOfU))
	sp = np.fft.ifft(hOfU)
	freq = np.fft.fftfreq(t.shape[-1])
	plt.title("H(u)")

		#calculate magnitude
	plt.plot(reals)
	plt.show()
	magnitude = []
	for x,y in zip(sp.real,sp.imag):
		magnitude.append(sqrt(x**2+y**2))
	#plot magnitude
	plt.plot(freq, magnitude)
	plt.title("Magnitude {0}".format("inverse"))
	plt.show()



N=128
t = np.arange(N)
#part1(np.sin(2*pi*8*t/N),"sin(2*pi*8*t/N)")
#part1(np.cos(2*pi*8*t/N),"cos(2*pi*8*t/N)")
#part1(np.cos(2*pi*8*t/N) + 3*np.sin(2*pi*8*t/N),"cos(2*pi*8*t/N) + sin(2*pi*8*t/N)")
#part2()
#part3()
#part4()
part5()






