import Image
from decimal import *

kRedConvert = 0.299
kGreenConvert = 0.587
kBlueConvert = 0.114

class PPMImage(object):
	r_histogram = []
	g_histogram = []
	b_histogram = []
	grey_histogram = []

	"""Class that holds for PPMImage"""
	def __init__(self, filename):
		super(PPMImage, self).__init__()
		print "Creating image..."
		self.filename = filename
		self.pixels=[]
		self.image = Image.open(self.filename)
		self.width = self.image.size[0]
		self.height = self.image.size[1]
 		print self.image.format, self.image.size, self.image.mode
 		self.outImage = Image.new('L', (self.width, self.height)) # Create a blank image
 		#rgbaG
 		self.setup_histograms()


 		print "Finished Creation"
 		self.image.show()
 	def setup_histograms(self):
 		self.r_histogram = [0] * 256
 		self.g_histogram = [0] * 256
 		self.b_histogram = [0] * 256
 		self.grey_histogram = [0] * 256
 	def convert_to_greyscale(self):
 		pix = self.outImage.load()
 		for i in range(0,self.height):
 			for j in range(0,self.width):
 				pixel = self.image.getpixel((j,i))
 				grey = kRedConvert * pixel[0]+ kGreenConvert * pixel[1] + kBlueConvert * pixel[2]
 				pix[j,i]= grey
 				#self.histogram[int(grey)][4]+=1
 		self.outImage.show()

 	def generate_histograms(self):
 		self.setup_histograms()
 		for i in range(0,self.height):
 			for j in range(0,self.width):
 				pixel = self.image.getpixel((j,i))
 				if type(pixel) == int:
 					self.grey_histogram[int(pixel)] += 1
 				else:
 					grey = kRedConvert * pixel[0]+ kGreenConvert * pixel[1] + kBlueConvert * pixel[2]
					self.grey_histogram[int(grey)] += 1
					self.r_histogram[int(pixel[0])] +=1
 					self.g_histogram[int(pixel[1])] +=1
 					self.b_histogram[int(pixel[2])] +=1

 	def write_to_path(self,filename):
 		self.outImage.save(filename)
 	
 	def write_full_histogram(self,filename):	
 		outFile = open(filename,'w')
 		for i in self.histogram:
 			for val in i:
 				outFile.write(str(val)+",")
 			outFile.write("\n")

 		outFile.close()


	def write_grey_histogram(self,filename):	
 		outFile = open(filename,'w')
 		for i in self.grey_histogram:
 			outFile.write(str(i)+",\n")
 		outFile.close()

	def generate_cumulative_histogram(self):
		self.generate_histograms()
		greys = self.grey_histogram
		cumulative_histogram=[greys[0]]
		for i in range(1,len(greys)):
			cumulative_histogram.append(greys[i]+cumulative_histogram[i-1])

		return cumulative_histogram

	def calculate_percentages(self, cumulative_histogram):
		grey_lookup = []
		for i in cumulative_histogram:
			area = self.width* self.height
			val = Decimal(i)/Decimal(area)
			grey_lookup.append(val)
		return grey_lookup

	def generate_lookups(self, grey_lookup):
		for i in range(0,len(grey_lookup)):
			grey_lookup[i]=grey_lookup[i]*255
		return grey_lookup

	def apply_lookups(self, lookups):
		pix = self.outImage.load()
 		for i in range(0,self.height):
 			for j in range(0,self.width):
 				pixel = self.image.getpixel((j,i))
 				pix[j,i]= lookups[pixel]
 				#self.histogram[int(grey)][4]+=1
 		self.outImage.show()
 		self.image = self.outImage


