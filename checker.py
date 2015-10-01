from PIL import Image
from fractions import gcd
from functions import *
from algorithms import *
import os, sys, math, io, string

#####################################################################################################
############################Function version for implementation######################################
#####################################################################################################
def scanXth(pixList):
	for xth in range(2, 21):
		#print("Checking channel " + str(xth))
		f = xthPixelRetrieve([pixList, 300, [xth]], silent=True)
		#Split off the non-filename component
		try:
			#######Filename Length Validity Check######
			if(f[0] > 300):
				raise Exception("Filename Too Long")
			###########################################
			rawName = f[1:f[0] + 1]
			fileName = ''.join([chr(x) for x in rawName])
			########Filename Printability Check########
			for c in fileName:
				if(not c in string.printable):
					raise Exception("Filename Unprintable")
				else:
					#print(c)
					pass
			###########################################
			return (True, fileName, xth)
		except Exception as e:
			#print(e)
			continue
	return (False, "none", 0)
#This should only be used for (everyxthpixel)
def scanInColor(pixList, color, dist):
	#print("Checking channel " + str(xth))
	f = inColorRetrieve([pixList, 300, [color, dist]], silent=True)
	#Split off the non-filename component
	try:
		#######Filename Length Validity Check######
		if(f[0] > 300):
			raise Exception("Filename Too Long")
		###########################################
		rawName = f[1:f[0] + 1]
		fileName = ''.join([chr(x) for x in rawName])
		########Filename Printability Check########
		for c in fileName:
			if(not c in string.printable):
				raise Exception("Filename Unprintable")
			else:
				#print(c)
				pass
		###########################################
		return (True, fileName)
	except Exception as e:
		pass
	return (False, "none")
#This should only be used for (everyxthpixel)
def determineBestChannel(xSize, ySize, pattern, fileSize): 
	if(getMaxBytesGivenPattern(xSize * ySize, 4, pattern, 2) < fileSize):
		return -1
	best = 2 #Largest Channel
	for x in range(3, 21):
		next = ((xSize*ySize) - 3) / x #Near-perfect approximation for the normal modulo operation
		if(next > fileSize):
			best = x
		else:
			break
	return best
##########################################################################
args = sys.argv
#######################################
#########Get Algorithm Options#########
#######################################
#print(args)
alg = args.pop(len(args) - 1)
if(alg == "xth"):
	try:
		xth = int(args.pop(len(args) - 1))
		if(not xth == -1): #If there is a real override, measure it for validity
			if(xth < 2 or xth > 20):
				raise Exception("Spacer out of range.")
	except:
		print("Override value invalid. Number must be between 2 and 20")
		os._exit(1)
elif(alg == "inColor"):
	dist = args.pop(len(args) - 1)
	B = args.pop(len(args) - 1)
	G = args.pop(len(args) - 1)
	R = args.pop(len(args) - 1)
	#print(str(R) + ", " + str(G) + ", " + str(B) + ", " + str(dist))
	algArgs = str(R) + " " + str(G) + " " + str(B) + " " + str(dist)
	#print(args)
else:
	print("Algorithms other than xth not yet supported.")
	os._exit(1)

#There'll also eventually be more here as well
##########################
#######Testing Files######
##########################
if(args[1] == "inject"):
	if(not os.path.isfile(args[2])):
		print(str(args[2]) + " does not exist")
		os._exit(1)
	if(not os.path.isfile(args[3])):
		print(str(args[3]) + " does not exist")
		os._exit(1)
elif(args[1] == "retrieve"):
	if(not os.path.isfile(args[2])):
		print(str(args[2]) + " does not exist")
		os._exit(1)
elif(args[1] == "check"):
	if(not os.path.isfile(args[2])):
		print(str(args[2]) + " does not exist")
		os._exit(1)
##########################
##Opening the image file##
##########################
try:
	myImage = Image.open(str(args[2]))
	myImage = myImage.convert("RGB")
	xSize, ySize = myImage.size
	print("Image Properties:\n    Name:   " + str(args[2]) + "\n    Width:  " + str(xSize) + "\n    Height: " + str(ySize))
except:
	print(str(args[2]) + " is not a valid image file.")
	os._exit(1)
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
##################################
#####Special Brute Force Code#####
##################################
#Select the best channel if requested to
if(alg == "xth"):
	if(args[1] == "inject"):
		#xth = 0 #Initialize the xth argument
		#Get the size of the file to be injected
		fileSize = os.path.getsize(args[3])
		fileSize += len(args[3]) + 1
		if(xth == -1): #If we're gonna try to select the best
			#Determine the best channel
			xth = determineBestChannel(xSize, ySize, xthPattern, fileSize)
			if(xth == -1): #If there is no best
				#Display the max
				maxBytes = getMaxBytesGivenPattern(xSize * ySize, 4, xthPattern, 2)
				print("    " + str(maxBytes) + "/" + str(xSize * ySize) + " bytes available for writing on channel " + str(2) + ".")
				print("File properties:\n    Name: " + args[3] + "\n    Size: " + str(fileSize) + " bytes")
				print(str(fileSize) + " bytes exceeds max possible storage.")
				print(args[3] + " is too large to be injected into " + args[2])
				#Exit
				os._exit(1)
			else: ##If we found the best
				maxBytes = getMaxBytesGivenPattern(xSize * ySize, 4, xthPattern, xth)
		else: #Otherwise, if there's an override, just use it.
			maxBytes = getMaxBytesGivenPattern(xSize * ySize, 4, xthPattern, xth)
		#Check for the 2 states which don't auto-determine max size
		if(maxBytes < fileSize):
			#Display the max
			print("    " + str(maxBytes) + "/" + str(xSize * ySize) + " bytes available for writing on channel " + str(xth) + ".")
			print("File properties:\n    Name: " + args[3] + "\n    Size: " + str(fileSize) + " bytes")
			print(str(fileSize) + " bytes exceeds max possible storage.")
			print(args[3] + " is too large to be injected into " + args[2])
			#Exit
			os._exit(1)
	else:
		#For all other modes, simply default to 2 or whatever the overrride is
		try:
			if(not xth == -1):
				if(xth < 2 or xth > 20):
					raise Exception("Spacer out of range.")
			else:
				xth = 2
		except:
			print("Override value invalid. Number must be between 2 and 20")
			os._exit(1)
		maxBytes = getMaxBytesGivenPattern(xSize * ySize, 4, xthPattern, xth)
	print("    " + str(maxBytes) + "/" + str(xSize * ySize) + " bytes available for writing on channel " + str(xth) + ".")
	algArgs = str(xth)
elif(alg == "inColor"):
	if(args[1] == "inject"):
		fileSize = os.path.getsize(args[3])
		fileSize += len(args[3]) + 1
		maxBytes = getMaxBytesGivenColor(xSize * ySize, pixList, 4, inColorPattern, [(int(R), int(G), int(B)), int(dist)])
		print("    " + str(maxBytes) + "/" + str(xSize * ySize) + " bytes available for writing.")
	else:
		maxBytes = getMaxBytesGivenColor(xSize * ySize, pixList, 4, inColorPattern, [(int(R), int(G), int(B)), int(dist)])
		print("    " + str(maxBytes) + "/" + str(xSize * ySize) + " bytes available for writing.")
##################################
##Determine Injection Parameters##
##################################
if(same and byteNum < 999999999):
	if(alg == "xth"):
	###################################
	##If there is a stored file logic##
	###################################
		#Pasted from Retriever, repurposed for finding filename
		result = scanXth(pixList)
		if(result[0] == True):
			algArgs = str(result[2])
			print("Stored File Detected:")
			print("    Stored File Name:    " + result[1])
			print("    Stored File Size:    " + str(byteNum) + " bytes")
			print("    Stored File Channel: " + str(result[2]))
			if(args[1] == "inject"):
				print("Cannot write over already injected file.")
				os._exit(1) #Kill it DEAD
			elif(args[1] == "retrieve"):
				if(len(args) == 4):
					print("File will be written to " + args[3])
					os.system("retriever.py \"" + args[2] + "\" \"" + args[3] + "\" " + algArgs + " " + alg)
				else:
					print("File will be written to " + result[1])
					os.system("retriever.py \"" + args[2] + "\" \"" + result[1] + "\" " + algArgs + " " + alg)
		else:
			print("No Stored File.")
			if(args[1] == "inject"):
				print("File properties:\n    Name: " + args[3] + "\n    Size: " + str(fileSize) + " bytes")
				print(str(fileSize) + "/" + str(maxBytes) + " bytes to be used.")
				os.system("injector.py \"" + args[2] + "\" \"" + args[3] + "\" \"" + args[4] + "\" " + algArgs + " " + alg)
			elif(args[1] == "retrieve"):
				print("No file to retrieve.")
	elif(alg == "inColor"):
		result = scanInColor(pixList, (int(R), int(G), int(B)), int(dist))
		if(result[0] == True):
			print("Stored File Detected:")
			print("    Stored File Name:    " + result[1])
			print("    Stored File Size:    " + str(byteNum) + " bytes")
			if(args[1] == "inject"):
				print("Cannot write over already injected file.")
				os._exit(1) #Kill it DEAD
			elif(args[1] == "retrieve"):
				if(len(args) == 4):
					print("File will be written to " + args[3])
					os.system("retriever.py \"" + args[2] + "\" \"" + args[3] + "\" " + algArgs + " " + alg)
				else:
					print("File will be written to " + result[1])
					os.system("retriever.py \"" + args[2] + "\" \"" + result[1] + "\" " + algArgs + " " + alg)
		else:
			print("No Stored File.")
			if(args[1] == "inject"):
				print("File properties:\n    Name: " + args[3] + "\n    Size: " + str(fileSize) + " bytes")
				print(str(fileSize) + "/" + str(maxBytes) + " bytes to be used.")
				os.system("injector.py \"" + args[2] + "\" \"" + args[3] + "\" \"" + args[4] + "\" " + algArgs + " " + alg)
			elif(args[1] == "retrieve"):
				print("No file to retrieve.")
	else:
		print("Algorithms other than xth not yet supported.")
		os._exit(1)
else:
####################################
##If there is no stored file logic##
####################################
	print("No Stored File.")
	if(args[1] == "inject"):
		fileSize = os.path.getsize(args[3])
		fileSize += len(args[3]) + 1
		print("File properties:\n    Name: " + args[3] + "\n    Size: " + str(fileSize) + " bytes")
		print(str(fileSize) + "/" + str(maxBytes) + " bytes to be used.")
		os.system("injector.py \"" + args[2] + "\" \"" + args[3] + "\" \"" + args[4] + "\" " + algArgs + " " + alg)
	elif(args[1] == "retrieve"):
		print("No file to retrieve.")