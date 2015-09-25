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
pixList = myImage.getdata()
valIndex = 0

#####################
##Get The file size##
#####################
col1 = pixList[0]
col2 = pixList[1]
col3 = pixList[2]
if(colorGreaterThan(pixList[3], (9, 9, 9))):
	col1 = addColor(col1, (9, 9, 9))
	col2 = addColor(col2, (9, 9, 9))
	col3 = addColor(col3, (9, 9, 9))
if(headerColorIsSpecial(pixList[3])):
	col1 = dataFromSpecialHeader(col1, pixList[3])
	col2 = dataFromSpecialHeader(col2, pixList[3])
	col3 = dataFromSpecialHeader(col3, pixList[3])
else:
	col1 = subtractColor(col1, pixList[3])
	col2 = subtractColor(col2, pixList[3])
	col3 = subtractColor(col3, pixList[3])
byteNum = (colorTupleToBase10(col3) * 1000000) + (colorTupleToBase10(col2) * 1000) + colorTupleToBase10(col1)
print("Total Number of bytes to receive: " + str(byteNum))

######################################
##Display final prompt before action##
######################################
input("Press Enter to continue")

#xC, yC = 0, 0
for n in range(4, len(pixList)):
	try:
		x, y, z = pixList[n]
		if(valIndex >= byteNum):
			print("\n" + str(byteNum) + " bytes retrieved.")
			break
		if(matchesPattern(n)):
			#Extract data from a pixel
			baseColor = averageColor(pixList[n - 1], pixList[n + 1])
			subColor = subtractColor((x, y, z), baseColor)
			if(colorGreaterThan(baseColor, (7, 7, 5))):
				dataColor = addColor(subColor, (7, 7, 5))
			else:
				#Reverses special cases
				if(baseColorIsSpecial(baseColor)):
					dataColor = dataFromSpecialCase((x, y, z), baseColor)
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
		#file.write(bytearray(f))
		exit()
#Split the array into filename and data components
nameLength = (f[0] + 1)
rawName = f[1:nameLength]
f = f[nameLength:]
#Logic for overriding filename if applicable
try:
	file = io.open(str(args[2]), 'wb')
except:
	fileName = ""
	for x in range(len(rawName)):
		fileName += str(chr(rawName[x]))
	file = io.open(fileName, 'wb')
file.write(bytearray(f))
