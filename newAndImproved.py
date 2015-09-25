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

#############################
##Opening the injectee file##
#############################
file = io.open(str(args[2]), 'rb')
intFiList = []
intFiList.append(len(args[2]))
for c in str(args[2]):
	intFiList.append(ord(c))
intFiList.extend(list(file.read()))
#intFiList = list(file.read())
pixList = myImage.getdata()

###################################
##Determine injectability of file##
###################################
maxBytes = getMaxBytesGivenPattern(xSize * ySize, 3, matchesPattern)
print(str(maxBytes) + "/" + str(xSize * ySize) + " bytes available for writing.")
byteNum = len(intFiList)
if (byteNum > maxBytes):
	print(str(byteNum) + " exceeds max bytes available for writing.")
	exit()
print(str(byteNum) + "/" + str(maxBytes) + " bytes to be used.")
valIndex = 0

####################################
##Set up the injecting environment##
####################################
copyImage = Image.new('RGB', myImage.size)
newPixList = []

#############################
##Put in the file size data##
#############################
ones = byteNum%1000
millions = (byteNum - (byteNum%1000000))/1000000
thousands = (byteNum - (byteNum%1000) - (millions * 1000000))/1000
col1 = base10ToColorTuple(ones) #First 3 digits
col2 = base10ToColorTuple(thousands) #middle 3 digits
col3 = base10ToColorTuple(millions) #last 3 digits
##Replace the first 3 pixels with the fourth
newPixList.append(pixList[3])
newPixList.append(pixList[3])
newPixList.append(pixList[3])
newPixList.append(pixList[3])
if(colorGreaterThan(pixList[3], (9, 9, 9))):
	newPixList[0] = subtractColor(newPixList[0], (9, 9, 9))
	newPixList[1] = subtractColor(newPixList[1], (9, 9, 9))
	newPixList[2] = subtractColor(newPixList[2], (9, 9, 9))
if(headerColorIsSpecial(newPixList[3])):
	newPixList[0] = specialCaseHeaderColor(newPixList[0], col1)
	newPixList[1] = specialCaseHeaderColor(newPixList[1], col2)
	newPixList[2] = specialCaseHeaderColor(newPixList[2], col3)
else:
	newPixList[0] = addColor(newPixList[0], col1)
	newPixList[1] = addColor(newPixList[1], col2)
	newPixList[2] = addColor(newPixList[2], col3)

######################################
##Display final prompt before action##
######################################
input("Press Enter to continue...")

##########################
##Add File Data to Image##
##########################
for n in range(4, len(pixList)):
	x, y, z = pixList[n]
	if(matchesPattern(n)):#(n + 1)%3==0):#(n + 1) % (pixelSpace + pixelShift) == 0):
		#Write the data to a pixel
		if(valIndex < len(intFiList)):
			neighborAverage = averageColor(pixList[n - 1], pixList[n + 1])
			if(colorGreaterThan(neighborAverage, (7, 7, 5))):
				baseColor = subtractColor(neighborAverage, (7, 7, 5))
			else:
				baseColor = neighborAverage
			dataColor = base7ToColorTuple(intFiList[valIndex])
			#Handles very special cases
			if(baseColorIsSpecial(baseColor)):
				finalColor = specialCaseFinalColor(baseColor, dataColor)
			else:
				finalColor = addColor(baseColor, dataColor)
			newPixList.append(finalColor)
			valIndex += 1
			sys.stdout.write("\r" + str(int((valIndex/byteNum) * 100)) + "% Complete")
			sys.stdout.flush()
		else:
			newPixList.append((x, y, z))
	else:
		newPixList.append((x, y, z))
print("!") #To satisfy my autism
copyImage.putdata(newPixList)
copyImage.save(str(args[3]))