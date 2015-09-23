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
	
def base7ToColorTuple(num):
	color = [0, 0, 0]
	
	hundreds = (num - (num%49))/49
	color[2] = int(hundreds)
	num -= hundreds * 49
	
	tens = (num - (num%7))/7
	color[1] = int(tens)
	num -= tens * 7
	
	color[0] = int(num)
	
	return tuple(color)
def colorTupleToBase7(colorTuple):
	return (colorTuple[0] + (colorTuple[1] * 7) + (colorTuple[2] * 49))
def colorGreaterThan(color, comparison):
	for x in range(len(color)):
		if(color[x] < comparison[x]):
			return False
	return True
##END DEFS

#Getting some basic info
myImage = Image.open("out.png")
#myImage = myImage.convert("RGB")
xSize, ySize = myImage.size
print("Width: " + str(xSize) + " Height: " + str(ySize) + " Total Pixel Number: " + str(xSize * ySize))

f = []
file = open("hidden.txt", 'w')
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
		if((n+1)%3 == 0):#(n + 1) % (pixelSpace + pixelShift) == 0):
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
			print(chr(data))
			f.append(str(chr(data)))
			valIndex += 1
			pixelShift = getNewShift(pixelShift)
			#######################
		else:
			pass
	except:
		outString = ''.join(f)
		file.write(outString)
		file.write("ERROR! TOTAL CHARS READ: " + str(valIndex))
		exit()
	xC += 1
	if(xC > (xSize - 1)):
		xC = 0
		yC += 1
outString = ''.join(f)
file.write(outString)
