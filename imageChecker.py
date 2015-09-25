from PIL import Image
from fractions import gcd
from crazyFunctions import *
import os, sys, math, io

args = sys.argv

##########################
##Opening the image file##
##########################
myImage = Image.open(str(args[1]))
myImage = myImage.convert("RGB")
xSize, ySize = myImage.size
print("Image Dimensions:\n    Width: " + str(xSize) + " Height: " + str(ySize))

if(args[2] == "m"):
	maxBytes = getMaxBytesGivenPattern(xSize * ySize, 4, matchesPattern)
	print(str(maxBytes) + "/" + str(xSize * ySize) + " bytes available for writing.")
elif(args[2] == "c"):
	#There is a faster way to do this but I just want it to work
	pixList = myImage.getdata()
	col1 = pixList[0]
	col2 = pixList[1]
	col3 = pixList[2]
	if(colorGreaterThan(pixList[3], (9, 9, 9))):
		col1 = addColor(col1, (9, 9, 9))
		col2 = addColor(col2, (9, 9, 9))
		col3 = addColor(col3, (9, 9, 9))
	ccol1 = col1
	ccol2 = col2
	ccol3 = col3
	if(headerColorIsSpecial(pixList[3])):
		col1 = dataFromSpecialHeader(col1, pixList[3])
		col2 = dataFromSpecialHeader(col2, pixList[3])
		col3 = dataFromSpecialHeader(col3, pixList[3])
	else:
		col1 = subtractColor(col1, pixList[3])
		col2 = subtractColor(col2, pixList[3])
		col3 = subtractColor(col3, pixList[3])
	byteNum = (colorTupleToBase10(col3) * 1000000) + (colorTupleToBase10(col2) * 1000) + colorTupleToBase10(col1)
	ccol1 = subtractColor(ccol1, col1)
	ccol2 = subtractColor(ccol2, col2)
	ccol3 = subtractColor(ccol3, col3)
	same = True
	for x, y, z, q in zip(ccol1, ccol2, ccol3, pixList[3]):
		same = False
		if(x==y and x==z and x==q):
			same = True
	if(same and byteNum < 999999999):
		#May have false positives, but unlikely
		print("Stored File Size: " + str(byteNum) + " bytes")
	else:
		print("No Stored File.")
else:
	print("Invalid Mode.")