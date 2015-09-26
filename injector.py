from PIL import Image
from crazyFunctions import *
import sys, io

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
for n in range(4, len(pixList)):
	x, y, z = pixList[n]
	if(matchesPattern(n)):
		#Write the data to a pixel
		if(valIndex < len(intFiList)):
			baseColor = averageColor(pixList[n - 1], pixList[n + 1])
			dataColor = colorTupleFromValue(intFiList[valIndex], 7)
			finalColor = injectDataColorBaseX(baseColor, dataColor, 7)
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