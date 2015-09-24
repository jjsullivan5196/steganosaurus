from PIL import Image
from fractions import gcd
from crazyFunctions import *
import os, sys, math
##DEFS
#Returns the sum of a tuple
##END DEFS
args = sys.argv

#Getting some basic info
myImage = Image.open(str(args[1]))
#myImage = Image.open("pleasekillme.png")
myImage = myImage.convert("RGB")
xSize, ySize = myImage.size
print("Width: " + str(xSize) + " Height: " + str(ySize) + " Total Pixel Number: " + str(xSize * ySize))

#file = open("hello.txt", 'r')
file = open(str(args[2]), 'r')
fiList = list(file.readline())
intFiList = []
for e in fiList:
	intFiList.append(ord(e))
#print(intFiList)
#Determining info for pixel selection
maxBytes = xSize * ySize / 3
byteNum = len(intFiList) #Change this to see byte dist
if (byteNum > maxBytes):
	exit()
pixelSpace = int(xSize * ySize / byteNum)
pixelShift = 0
pixList = myImage.getdata()
valIndex = 0

copyImage = Image.new('RGB', myImage.size)
newPixList = []
xC, yC = 3, 0
dataPixList = []
#############################
##Put in the file size data##
#############################
col1 = base10ToColorTuple(byteNum%1000) #First 3 digits
col2 = base10ToColorTuple((byteNum - (byteNum%1000))/1000) #Last 3 digits
##Replace the first 2 pixels with the third
newPixList.append(pixList[2])
newPixList.append(pixList[2])
newPixList.append(pixList[2])
newPixList[0] = subtractColor(newPixList[0], (9, 9, 9))
newPixList[1] = subtractColor(newPixList[1], (9, 9, 9))
newPixList[0] = addColor(newPixList[0], col1)
newPixList[1] = addColor(newPixList[1], col2)
##########################
##Add File Data to Image##
##########################
for n in range(3, len(pixList)):
	x, y, z = pixList[n]
	if(matchesPattern(n)):#(n + 1)%3==0):#(n + 1) % (pixelSpace + pixelShift) == 0):
		#Write the data to a pixel
		if(valIndex < len(intFiList)):
			print(str(xC) + " " + str(yC))
			print("Original RGB values " + str((x, y, z)))
			neighbor1, neighbor2 = pixList[n - 1], pixList[n + 1]
			print(str(neighbor1) + " " + str(neighbor2))
			print("Average Neighbor Color: " + str(averageColor(neighbor1, neighbor2)))
			##Make sure the color is bright enough, if not just throw the thing on top
			if(colorGreaterThan(averageColor(neighbor1, neighbor2), (7, 7, 5))):
				baseColor = subtractColor(averageColor(neighbor1, neighbor2), (7, 7, 5))
			else:
				baseColor = averageColor(neighbor1, neighbor2)
			print("Data color to be added: " + str(base7ToColorTuple(intFiList[valIndex])))
			dataColor = addColor(baseColor, base7ToColorTuple(intFiList[valIndex]))
			print(dataColor)
			newPixList.append(dataColor)
			valIndex += 1
			pixelShift = getNewShift(pixelShift)
			#Not strictly necessary
			if not (xC, yC) in dataPixList:
				dataPixList.append((xC, yC))
			else:
				print("Pixel Value Repeated")
				exit()
		else:
			newPixList.append((x, y, z))
		#######################
	else:
		newPixList.append((x, y, z))
	xC += 1
	if(xC > (xSize - 1)):
		xC = 0
		yC += 1
copyImage.putdata(newPixList)
copyImage.save(str(args[3]))
print("Base Color " + str(pixList[2]))
print(byteNum)
print(col1)
print(newPixList[0])
print(col2)
print(newPixList[1])
input("Press Enter to continue...")