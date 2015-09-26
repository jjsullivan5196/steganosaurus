from PIL import Image
from crazyFunctions import *
import sys, io

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
col1 = retrieveDataColorBaseX(pixList[0], pixList[3], 10)
col2 = retrieveDataColorBaseX(pixList[1], pixList[3], 10)
col3 = retrieveDataColorBaseX(pixList[2], pixList[3], 10)
byteNum = (colorTupleBaseXToVal(col3, 10) * 1000000) + (colorTupleBaseXToVal(col2, 10) * 1000) + colorTupleBaseXToVal(col1, 10)
print("Total Number of bytes to receive: " + str(byteNum))

######################################
##Display final prompt before action##
######################################
input("Press Enter to continue")

for n in range(4, len(pixList)):
	try:
		x, y, z = pixList[n]
		if(valIndex >= byteNum):
			print("\n" + str(byteNum) + " bytes retrieved.")
			break
		if(matchesPattern(n)):
			#Extract data from a pixel
			baseColor = averageColor(pixList[n - 1], pixList[n + 1])
			dataColor = retrieveDataColorBaseX((x, y, z), baseColor, 7)
			data = colorTupleBaseXToVal(dataColor, 7)
			f.append(data)
			valIndex += 1
			sys.stdout.write("\r" + str(int((valIndex/byteNum) * 100)) + "% Complete")
			sys.stdout.flush()
		else:
			pass
	except:
		print("\nERROR: Could not retrieve bytes.")
		print(str(valIndex) + "/" + str(byteNum) + " bytes retrieved before Error.")
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
try:
	file.write(bytearray(f))
except:
	print("Could not write bytes to file.")