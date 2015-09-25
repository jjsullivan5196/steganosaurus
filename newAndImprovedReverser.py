from PIL import Image
from fractions import gcd
from crazyFunctions import *
import os, sys, math, io

args = sys.argv
##########################
##Opening the image file##
##########################
myImage = Image.open(args[1])
xSize, ySize = myImage.size
print("Image Dimensions:\n    Width: " + str(xSize) + " Height: " + str(ySize))

###########################
##Opening the output file##
###########################
f = []
file = io.open(str(args[2]), 'wb')
pixList = myImage.getdata()
valIndex = 0

#####################
##Get The file size##
#####################
col1 = pixList[0]
col2 = pixList[1]
col1 = addColor(col1, (9, 9, 9))
col2 = addColor(col2, (9, 9, 9))
col1 = subtractColor(col1, pixList[2])
col2 = subtractColor(col2, pixList[2])
byteNum = (colorTupleToBase10(col2) * 1000) + colorTupleToBase10(col1)
print("Total Number of bytes to receive: " + str(byteNum))

######################################
##Display final prompt before action##
######################################
input("Press Enter to continue")

#xC, yC = 0, 0
for n in range(3, len(pixList)):
	try:
		x, y, z = pixList[n]
		if(valIndex >= byteNum):
			print("\n" + str(byteNum) + " bytes retrieved.")
			break
		if(matchesPattern(n)):
			#Extract data from a pixel
			avgColor = averageColor(pixList[n - 1], pixList[n + 1])
			subColor = subtractColor((x, y, z), avgColor)
			if(colorGreaterThan(avgColor, (7, 7, 5))):
				dataColor = addColor(subColor, (7, 7, 5))
			else:
				dataColor = subColor
			data = colorTupleToBase7(dataColor)
			f.append(data)
			valIndex += 1
			sys.stdout.write("\r" + str(int((valIndex/byteNum) * 100)) + "% Complete")
			sys.stdout.flush()
		else:
			pass
	except:
		print("\nERROR: Could not retrieve bytes.")
		print(str(valIndex) + "/" + str(byteNum) + " bytes retrieved.")
		file.write(bytearray(f))
		exit()
	'''
	xC += 1
	if(xC > (xSize - 1)):
		xC = 0
		yC += 1
	'''
file.write(bytearray(f))
