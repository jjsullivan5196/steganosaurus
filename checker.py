from PIL import Image
from fractions import gcd
from functions import *
import os, sys, math, io

args = sys.argv

##########################
##Opening the image file##
##########################
myImage = Image.open(str(args[1]))
myImage = myImage.convert("RGB")
##########################
##Determining Properties##
##########################
xSize, ySize = myImage.size
print("Image Properties:\n    Width: " + str(xSize) + " Height: " + str(ySize))
maxBytes = getMaxBytesGivenPattern(xSize * ySize, 4, matchesPattern)
print("    " + str(maxBytes) + "/" + str(xSize * ySize) + " bytes available for writing.")
#############################
##Checking for Stored Files##
#############################
pixList = myImage.getdata()
col1 = retrieveDataColorBaseX(pixList[0], pixList[3], 10)
col2 = retrieveDataColorBaseX(pixList[1], pixList[3], 10)
col3 = retrieveDataColorBaseX(pixList[2], pixList[3], 10)
byteNum = (colorTupleBaseXToVal(col3, 10) * 1000000) + (colorTupleBaseXToVal(col2, 10) * 1000) + colorTupleBaseXToVal(col1, 10)
bcol1 = retrieveBaseColor(pixList[0], col1, 10)
bcol2 = retrieveBaseColor(pixList[1], col2, 10)
bcol3 = retrieveBaseColor(pixList[2], col3, 10)
same = True
for x, y, z, q in zip(bcol1, bcol2, bcol3, pixList[3]):
	same = False
	if(x==y and x==z and x==q):
		same = True
#############################
##Printing Stored File Info##
#############################
if(same and byteNum < 999999999):
	#Pasted from Retriever, repurposed for finding filename
	f = []
	n = 4
	while(len(f) < 300):#300 is the maximum feasible filename including an INSANE 40 char extension
		try:
			x, y, z = pixList[n]
			if(matchesPattern(n)):
				#Extract data from a pixel
				baseColor = averageColor(pixList[n - 1], pixList[n + 1])
				dataColor = retrieveDataColorBaseX((x, y, z), baseColor, 7)
				data = colorTupleBaseXToVal(dataColor, 7)
				f.append(data)
				n += 1
			else:
				n += 1
		except:
			print("\nERROR: Could not retrieve bytes.")
			exit()
	#Split off the non-filename component
	rawName = f[1:f[0] + 1] #Oy Vey this is messy but it works
	fileName = ""
	for x in range(len(rawName)):
		fileName += str(chr(rawName[x]))
	print("Stored File Detected.")
	print("    Stored File Size: " + str(byteNum) + " bytes")
	print("    Stored File Name: " + fileName)
else:
	print("No Stored File.")