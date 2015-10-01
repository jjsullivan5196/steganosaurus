from PIL import Image
from functions import *
from algorithms import *
import sys, io

args = sys.argv #("retriever.py", "File", "Output Override")
##########################
#########Override#########
##########################
xth = int(args[len(args) - 1])
##########################
##Opening the image file##
##########################
myImage = Image.open(args[1])
xSize, ySize = myImage.size
#print("Image Dimensions:\n    Width: " + str(xSize) + " Height: " + str(ySize))

###########################
##Opening the output file##
###########################
f = []
pixList = myImage.getdata()
valIndex = 0

#####################
##Get The file size##
#####################
col1 = retrieveDataColorBaseX(pixList[0], pixList[3], 10)
col2 = retrieveDataColorBaseX(pixList[1], pixList[3], 10)
col3 = retrieveDataColorBaseX(pixList[2], pixList[3], 10)
byteNum = (colorTupleBaseXToVal(col3, 10) * 1000000) + (colorTupleBaseXToVal(col2, 10) * 1000) + colorTupleBaseXToVal(col1, 10)
#print("Total Number of bytes to receive: " + str(byteNum))

######################################
##Display final prompt before action##
######################################
input("Press Enter to continue")

############################
##Get File Data from Image##
############################
f = xthPixelRetrieve([pixList, byteNum, [xth]])

#Cut the filename component off the data
nameLength = (f[0] + 1)
f = f[nameLength:]
fileName = str(args[2])
file = io.open(fileName, 'wb')
try:
	file.write(bytearray(f))
	print("Bytes written to " + fileName)
except:
	print("Could not write bytes to file.")