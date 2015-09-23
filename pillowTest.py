from PIL import Image
import os, sys, math
##DEFS
#Gets the ratio of the values in a tuple
#Returns a tuple of the same size with the ratios
def getRatio(tup):
	smallest = 255
	for element in tup:
		if(element < smallest and element != 0):
			smallest = element
	list = []
	for element in tup:
		list.append(element/smallest)
	return tuple(list)
#Distributes an int according to a tuple ratio
#Returns a tuple with the int distributed inside according to the ratio
def distributeByRatio(amount, ratio):
	total = 0
	for num in ratio:
		total += num
	piece = amount/total
	l = []
	for num in ratio:
		l.append(piece * num)
	return tuple(l)
#Returns the sum of a tuple
def sumTup(tup):
	total = 0
	for e in tup:
		total += e
	return total
def avgTup(tup):
	total = 0
	for e in tup:
		total += e
	return total/len(tup)
def getNewShift(oldShift):
	#This is gonna have magic prime numbers
	ret = oldShift + 43 #Oh jeez look at all the magic
	if(ret > 100):
		ret -= 200
	return ret
##END DEFS

#Getting some basic info
myImage = Image.open("testImage.jpg")
xSize, ySize = myImage.size
print("Width: " + str(xSize) + " Height: " + str(ySize) + " Total Pixel Number: " + str(xSize * ySize))
#Determining info for pixel selection
maxBytes = xSize * ySize / 3
byteNum = 2000 #Change this to see byte dist
if (byteNum > maxBytes):
	exit()
pixelSpace = int(xSize * ySize / byteNum)
pixelShift = 0 #again, adjust for fun
pixList = myImage.getdata()
copyImage = Image.new('RGB', myImage.size)
newPixList = []
xC, yC = 0, 0
dataPixList = []
for n in range(len(pixList)):
	x, y, z = pixList[n]
	if((n + 1) % (pixelSpace + pixelShift) == 0):
		newPixList.append((255, 0, 0))
		pixelShift = getNewShift(pixelShift)
		print(str(xC) + " " + str(yC))
		if not (xC, yC) in dataPixList:
			dataPixList.append((xC, yC))
		else:
			print("Pixel Value Repeated")
			exit()
	else:
		newPixList.append((x, y, z))
	xC += 1
	if(xC > (xSize - 1)):
		xC = 0
		yC += 1
print("Width: " + str(xSize) + " Height: " + str(ySize) + " Total Pixel Number: " + str(xSize * ySize))
print(xSize * ySize)
copyImage.putdata(newPixList)
copyImage.save("out.png")