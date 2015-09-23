from PIL import Image
from fractions import gcd
import os, sys, math
##DEFS
#Returns the sum of a tuple
def sumTup(tup):
	total = 0
	for e in tup:
		total += e
	return total
#Returns the sum of a list
def sumList(list):
	total = 0
	for e in list:
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
def addLists(l1, l2):
	l = []
	for i in range(len(l1)):
		l.append(l1[i] + l2[i])
	return l
##Color operations
##Used for easy color changing
def averageColor(c1, c2):
	R = int((c1[0] + c2[0])/2)
	G = int((c1[1] + c2[1])/2)
	B = int((c1[2] + c2[2])/2)
	return (R, G, B)
def subtractColor(base, sub):
	R = (base[0] - sub[0])
	G = (base[1] - sub[1])
	B = (base[2] - sub[2])
	return (R, G, B)
def addColor(c1, c2):
	R = (c1[0] + c2[0])
	G = (c1[1] + c2[1])
	B = (c1[2] + c2[2])
	return (R, G, B)
#For the super-simple message length recording
def convertToBase255(number):
	pow2 = 0
	while(number >= 255):
		print(str(number) + " > 255")
		number -= 255
		pow2 += 1
	if(pow2 >= 255):
		while(pow2 >= 255):
			pow2 -= 255
			pow3 += 1
	else:
		pow3 = 0
	#(ones, 255s, 255^2s)
	return (number, pow2, pow3)
def convertFromBase255(threeTuple):
	return threeTuple[0] + (threeTuple[1]*255) + (threeTuple[2]*255*255)
#For NEW AND IMPROVED data hiding
def base10ToColorTuple(num):
	color = [0, 0, 0]
	
	hundreds = (num - (num%100))/100
	color[2] = int(hundreds)
	num -= hundreds * 100
	
	tens = (num - (num%10))/10
	color[1] = int(tens)
	num -= tens * 10
	
	color[0] = int(num)
	
	return tuple(color)
def colorTupleToBase10(colorTuple):
	return (colorTuple[0] + (colorTuple[1] * 10) + (colorTuple[2] * 100))
##END DEFS

#Getting some basic info
myImage = Image.open("pleasekillme.png")
#myImage = myImage.convert("RGB")
xSize, ySize = myImage.size
print("Width: " + str(xSize) + " Height: " + str(ySize) + " Total Pixel Number: " + str(xSize * ySize))

file = open("hello.txt", 'r')
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
xC, yC = 0, 0
dataPixList = []
for n in range(len(pixList)):
	x, y, z, a = pixList[n]
	if((n + 1)%3==0):#(n + 1) % (pixelSpace + pixelShift) == 0):
		#Write the data to a pixel
		if(valIndex < len(intFiList)):
			print(str(xC) + " " + str(yC))
			print("Original RGB values " + str((x, y, z)))
			neighbor1, neighbor2 = pixList[n - 1], pixList[n + 1]
			print(str(neighbor1) + " " + str(neighbor2))
			print("Average Neighbor Color: " + str(averageColor(neighbor1, neighbor2)))
			baseColor = subtractColor(averageColor(neighbor1, neighbor2), (9, 9, 2))
			print("Data color to be added: " + str(base10ToColorTuple(intFiList[valIndex])))
			dataColor = addColor(baseColor, base10ToColorTuple(intFiList[valIndex]))
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
		if(xC == 0 and yC == 0):
			newPixList.append(convertToBase255(byteNum))
		else:
			newPixList.append((x, y, z))
	xC += 1
	if(xC > (xSize - 1)):
		xC = 0
		yC += 1
copyImage.putdata(newPixList)
copyImage.save("out.png")
