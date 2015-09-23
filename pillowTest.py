from PIL import Image
from fractions import gcd
import os, sys, math
##DEFS
#Gets the ratio of the values in a tuple
#Returns a tuple of the same size with the ratios
def getRatio(tup):
	GCD = gcd(tup)
	list = []
	for element in tup:
		list.append(int(element/GCD))
	return tuple(list)
#Distributes an int according to a tuple ratio
#Returns a tuple with the int distributed inside according to the ratio
def distributeByRatio(amount, ratio):
	total = 0
	for num in ratio:
		total += num
	piece = int(amount/total)
	l = []
	for num in ratio:
		l.append(piece * num)
	#distributing the rest
	ind = 0
	remainder = amount % total
	if (remainder > 0):
		for x in range(remainder):
			l[ind] += 1
			ind += 1
			if(ind > 2):
				ind = 0
	#l[0] += amount%total
	return tuple(l)
#Oh jesus just kill me what the fuck
def adjustColorSum(amount, color):
	l = []
	for p in color:
		l.append(p)
	sum = sumTup(color)
	if(sum > amount):
		adj = -1
	else:
		adj = 1
	ind = 0
	while(sumList(l) != amount):
		if(adj == -1 and l[ind] <= 0):
			ind += 1
			if(ind > 2):
				ind = 0
			continue
		if(adj == 1 and l[ind] >= 255):
			ind += 1
			if(ind > 2):
				ind = 0
			continue
		l[ind] += adj
		ind += 1
		if(ind > 2):
			ind = 0
	return tuple(l)
#Returns the sum of a tuple
def sumTup(tup):
	total = 0
	for e in tup:
		total += e
	return total
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
def getBrightness(pixel):
	total = 0
	for p in pixel:
		total += p
	#print("Brightness is " + str(int(total/3)))
	return int(total/3)
def normalizeBrightness(mainColor, c1, c2):
	l = []
	cl1 = list(c1)
	cl2 = list(c2)
	adj = addLists(cl1, cl2)
	for i in range(len(adj)):
		adj[i] = int(adj[i]/2) #get the average of the two lists
		adj[i] = int(adj[i]*(2/3)) #reduce the value to make room for the byte
	l = addLists(list(mainColor), adj)
	return tuple(l)
##Gets a GCD from a color tuple
##probably a bit slow but required
##Also adjusts any odd number so it becomes even
def addLists(l1, l2):
	l = []
	for i in range(len(l1)):
		l.append(l1[i] + l2[i])
	return l
def gcd(threeTuple):
	threeTuple = (makeEven(threeTuple[0]), makeEven(threeTuple[1]), makeEven(threeTuple[2]))
	largest = 0
	for e in threeTuple:
		if(e > largest):
			largest = e
	gcd = 0
	for i in range(1, largest):
		if(threeTuple[0]%i == 0 and threeTuple[1]%i == 0 and threeTuple[2]%i == 0):
			if(i > gcd):
				gcd = i
	return gcd
def odd(num):
	if(num % 2 == 0):
		return False
	else:
		return True
def makeEven(num):
	if(odd(num)):
		return num-1
	else:
		return num
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
def makeSpecificGrey(value):
	list = [0, 0, 0]
	ind = 0
	while(sumList(list) < value):
		list[ind] += 1
		ind += 1
		if(ind > 2):
			ind = 0
	return tuple(list)
##END DEFS

#Getting some basic info
myImage = Image.open("testImage.png")
xSize, ySize = myImage.size
print("Width: " + str(xSize) + " Height: " + str(ySize) + " Total Pixel Number: " + str(xSize * ySize))

file = open("hello.txt", 'r')
fiList = list(file.readline())
intFiList = []
for e in fiList:
	intFiList.append(ord(e))
print(intFiList)
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
for n in range(1, len(pixList)):
	x, y, z, a = pixList[n] #Needs RGBA for PNG
	if((n + 1) % (pixelSpace + pixelShift) == 0):
		#Write the data to a pixel
		if(valIndex < len(intFiList)):
			print(str(xC) + " " + str(yC))
			print("Original RGB values " + str((x, y, z)))
			#print(getRatio((x, y, z)))
			newColor = adjustColorSum(intFiList[valIndex],(x, y, z))
			#newColor = makeSpecificGrey(intFiList[valIndex])
			print("Adjusted RGB values " + str(newColor))
			neighbor1, neighbor2 = pixList[n - 1], pixList[n + 1]
			newColorAdj = normalizeBrightness(newColor, neighbor1, neighbor2)
			newPixList.append(newColorAdj)
			print("Normalized RGB values " + str(newColorAdj))
			print(sumTup(newColor))
			print(chr(intFiList[valIndex]))
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