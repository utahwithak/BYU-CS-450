import Image
from PPMImage import *
import sys

if len(sys.argv) != 3:
	print "Invalid use: ImageBasics.py <in-path> <out-path>"
	sys.exit(-1)

if sys.argv[1][-3:] != "pgm":
	print "Invalid input file, must be .ppm or .pgm"
	sys.exit(-1)


print "Loading image at path:",sys.argv[1]
image = PPMImage(sys.argv[1])
image.generate_histograms()
image.write_grey_histogram("preequalized.csv")

#generate cumulative values
cumulative_histogram = image.generate_cumulative_histogram()

lookups = image.calculate_percentages(cumulative_histogram)

lookup_vals = image.generate_lookups(lookups)

image.apply_lookups(lookup_vals)


print "Writing pgm to path: ",sys.argv[2]
image.write_to_path(sys.argv[2])
image.generate_histograms()
print "Writing grey histogram to path: ",sys.argv[2],".csv"
image.write_grey_histogram("afterequalized.csv")

print "Done"


