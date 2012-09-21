import Image

kRedConvert = 0.299
kGreenConvert = 0.587
kBlueConvert = 0.114

class PPMImage(object):
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
 		self.histogram = []
 		for i in range(0,256):
 			self.histogram.append([0,0,0,0,0])
 		print "Finished Creation"
 		self.image.show()

 	def convert_to_greyscale(self):
 		#import pdb; pdb.set_trace()
 		pix = self.outImage.load()
 		for i in range(0,self.height):
 			for j in range(0,self.width):
 				pixel = self.image.getpixel((j,i))
 				grey = kRedConvert * pixel[0]+ kGreenConvert * pixel[1] + kBlueConvert * pixel[2]
 				pix[j,i]= grey
 				#self.histogram[int(grey)][4]+=1
 		self.outImage.show()

 	def generate_full_histogram(self):
 		for i in range(0,self.height):
 			for j in range(0,self.width):
 				pixel = self.image.getpixel((j,i))
 				grey = kRedConvert * pixel[0]+ kGreenConvert * pixel[1] + kBlueConvert * pixel[2]
				self.histogram[int(pixel[0])][0] +=1
 				self.histogram[int(pixel[1])][1] +=1
 				self.histogram[int(pixel[2])][2] +=1
 				self.histogram[int(grey)][4] +=1
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
	 		for i in self.histogram:
	 			outFile.write(str(i[4])+",\n")
	 		outFile.close()
