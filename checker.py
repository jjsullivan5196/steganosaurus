from PIL import Image
from fractions import gcd
from functions import *
import os, sys, math, io

args = sys.argv

##########################
##Opening the image file##
##########################
myImage = Image.open(str(args[2]))
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
###################################
##If there is a stored file logic##
###################################
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
	try:
		rawName = f[1:f[0] + 1] #Oy Vey this is messy but it works
		fileName = ""
		for x in range(len(rawName)):
			fileName += str(chr(rawName[x]))
		print("Stored File Detected.")
		print("    Stored File Size: " + str(byteNum) + " bytes")
		print("    Stored File Name: " + fileName)
		if(args[1] == "inject"):
			print("Cannot write over already injected file.")
			os._exit(1) #Kill it DEAD
		elif(args[1] == "retrieve"):
			if(len(args) == 4):
				print("File will be written to " + args[3])
				os.system("retriever.py " + args[2] + " " + args[3])
			else:
				print("File will be written to " + fileName)
				os.system("retriever.py " + args[2] + " \"" + fileName + "\"")
	except:
		print("No Stored File.")
		if(args[1] == "inject"):
			fileSize = os.path.getsize(args[3])
			fileSize += len(args[3]) + 1
			print("File properties:\n    Name: " + args[3] + "\n    Size: " + str(fileSize))
			if(fileSize > maxBytes):
				print(str(fileSize) + "/" + str(maxBytes) + " bytes to be used.")
				print(args[3] + " is too large to be injected into " + args[2])
			else:
				print(str(fileSize) + "/" + str(maxBytes) + " bytes to be used.")
				os.system("injector.py " + args[2] + " " + args[3] + " " + args[4])
		elif(args[1] == "retrieve"):
			print("No file to retrieve.")
else:
####################################
##If there is no stored file logic##
####################################
	print("No Stored File.")
	if(args[1] == "inject"):
		fileSize = os.path.getsize(args[3])
		fileSize += len(args[3]) + 1
		print("File properties:\n    Name: " + args[3] + "\n    Size: " + str(fileSize))
		if(fileSize > maxBytes):
			print(str(fileSize) + "/" + str(maxBytes) + " bytes to be used.")
			print(args[3] + " is too large to be injected into " + args[2])
		else:
			print(str(fileSize) + "/" + str(maxBytes) + " bytes to be used.")
			os.system("injector.py " + args[2] + " " + args[3] + " " + args[4])
	elif(args[1] == "retrieve"):
		print("No file to retrieve.")