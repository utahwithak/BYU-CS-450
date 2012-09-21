import Image
from PPMImage import *
import sys

if len(sys.argv) != 3:
	print "Invalid use: ImageBasics.py <in-path> <out-path>"
	sys.exit(-1)

if sys.argv[1][-3:] != "ppm":
	print "Invalid input file, must be .ppm"
	sys.exit(-1)
if sys.argv[2][-3:] != "pgm":
	print "Invalid output file, must be .pgm"
	sys.exit(-1)

print "Loading image at path:",sys.argv[1]
image = PPMImage(sys.argv[1])

print "Converting Image..."
image.convert_to_greyscale()

print "Writing pgm to path: ",sys.argv[2]
image.write_to_path(sys.argv[2])

print "Writing grey histogram to path: ",sys.argv[2],".csv"
image.write_grey_histogram(sys.argv[2]+".csv")
image.generate_full_histogram()
image.write_full_histogram(sys.argv[2]+".csv")
print "Done"


