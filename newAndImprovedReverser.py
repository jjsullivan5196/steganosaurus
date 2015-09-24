from PIL import Image
from fractions import gcd
from crazyFunctions import *
import os, sys, math, io
##DEFS
#Returns the sum of a tuple
#Getting some basic info
args = sys.argv
myImage = Image.open(args[1])
#myImage = Image.open("out.png")
#myImage = myImage.convert("RGB")
xSize, ySize = myImage.size
print("Width: " + str(xSize) + " Height: " + str(ySize) + " Total Pixel Number: " + str(xSize * ySize))

f = []
file = io.open(str(args[2]), 'wb')
#Determining info for pixel selection
maxBytes = xSize * ySize / 3
pixList = myImage.getdata()
#####################
##Get The file size##
#####################
print("Base Color " + str(pixList[2]))
col1 = pixList[0]
col2 = pixList[1]
col1 = addColor(col1, (9, 9, 9))
col2 = addColor(col2, (9, 9, 9))
col1 = subtractColor(col1, pixList[2])
col2 = subtractColor(col2, pixList[2])
byteNum = (colorTupleToBase10(col2) * 1000) + colorTupleToBase10(col1)

print("Total Number of bytes to receive: " + str(byteNum))
input("Press Enter to continue")
pixelSpace = int(xSize * ySize / byteNum)
pixelShift = 0
valIndex = 0

xC, yC = 0, 0
for n in range(3, len(pixList)):
	try:
		x, y, z = pixList[n]
		if(valIndex >= byteNum):
			print("All bytes retrieved")
			break
		if(matchesPattern(n)):#(n+1)%3 == 0):#(n + 1) % (pixelSpace + pixelShift) == 0):
			#Write the data to a pixel
			print(str(xC) + " " + str(yC))
			print("RGB values " + str((x, y, z)))
			neighbor1, neighbor2 = pixList[n - 1], pixList[n + 1]
			print(str(neighbor1) + " " + str(neighbor2))
			########################################
			avgColor = averageColor(neighbor1, neighbor2)
			print("Neighbor average color: " + str(avgColor))
			subColor = subtractColor((x, y, z), avgColor)
			print("Un-Offsetted Data Color: " + str(subColor))
			if(colorGreaterThan(avgColor, (7, 7, 5))):
				dataColor = addColor(subColor, (7, 7, 5))
			else:
				dataColor = subColor
			print("Data Color: " + str(dataColor))
			data = colorTupleToBase7(dataColor)
			#print(chr(data))
			f.append(data)#str(chr(data)))
			valIndex += 1
			pixelShift = getNewShift(pixelShift)
			#######################
		else:
			pass
	except:
		#outString = ''.join(f)
		#file.write(outString)
		file.write(bytearray(f))
		file.write("ERROR! TOTAL CHARS READ: " + str(valIndex))
		exit()
	xC += 1
	if(xC > (xSize - 1)):
		xC = 0
		yC += 1
#outString = ''.join(f)
file.write(bytearray(f))#outString)
