from PIL import Image
from functions import *
from algorithms import *
import sys, io, ntpath

args = sys.argv #("injector.py", "Host", "Injectee", "Output")
##########################
#########Override#########
##########################
#print(args)
alg = args.pop(len(args) - 1)
if(alg == "xth"):
	xth = int(args.pop(len(args) - 1))
elif(alg == "inColor"):
	dist = int(args.pop(len(args) - 1))
	B = int(args.pop(len(args) - 1))
	G = int(args.pop(len(args) - 1))
	R = int(args.pop(len(args) - 1))
##########################
##Opening the image file##
##########################
myImage = Image.open(str(args[1]))
myImage = myImage.convert("RGB")
xSize, ySize = myImage.size
#print("Image Dimensions:\n    Width: " + str(xSize) + " Height: " + str(ySize))

#############################
##Opening the injectee file##
#############################
file = io.open(str(args[2]), 'rb')
fileName = ntpath.basename(args[2]) #Takes the path off, so the path doesn't get appended with the file
intFiList = []
intFiList.append(len(fileName))
for c in str(fileName): 
	intFiList.append(ord(c))
intFiList.extend(list(file.read()))
pixList = myImage.getdata()

####################################
##Set up the injecting environment##
####################################
byteNum = len(intFiList) ##This should probably be passed in
copyImage = Image.new('RGB', myImage.size)
newPixList = []
valIndex = 0

#############################
##Put in the file size data##
#############################
ones = byteNum%1000
millions = (byteNum - (byteNum%1000000))/1000000
thousands = (byteNum - (byteNum%1000) - (millions * 1000000))/1000
col1 = colorTupleFromValue(ones, 10) #First 3 digits
col2 = colorTupleFromValue(thousands, 10) #middle 3 digits
col3 = colorTupleFromValue(millions, 10) #last 3 digits
##Replace the first 3 pixels with the fourth
newPixList.append(injectDataColorBaseX(pixList[3], col1, 10))
newPixList.append(injectDataColorBaseX(pixList[3], col2, 10))
newPixList.append(injectDataColorBaseX(pixList[3], col3, 10))
newPixList.append(pixList[3])

######################################
##Display final prompt before action##
######################################
input("Press Enter to continue...")

##########################
##Add File Data to Image##
##########################
if(alg == "xth"):
	newPixList = xthPixelInject([pixList, newPixList, intFiList, [xth]])
elif(alg == "inColor"):
	newPixList = inColorInject([pixList, newPixList, intFiList, [(R, G, B), dist]])
else:
	print("Algorithms other than xth not yet supported.")
	os._exit(1)

copyImage.putdata(newPixList)
copyImage.save(str(args[3]))