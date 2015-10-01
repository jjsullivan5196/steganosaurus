from functions import *
import sys, os
#This file contains all of the injection and retrieval algorithms used
def xthPixelInject(args = None): #args should be [pixList, newPixList, intFiList, [Relevant CLI Args as list]]
	pixList = args[0]
	newPixList = args[1]
	intFiList = args[2]
	xth = int(args[3][0]) #The only arg this accepts is X
	valIndex = 0
	byteNum = len(intFiList)
	for n in range(4, len(pixList)):
		x, y, z = pixList[n]
		if(xthPattern(n, xth)):
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
	return newPixList

def xthPixelRetrieve(args = None, silent = False):#args should be [pixList, byteNum, [Relevant CLI Args as list]]
	pixList = args[0]
	byteNum = args[1]
	xth = args[2][0]
	f = []
	valIndex = 0
	for n in range(4, len(pixList)):
		try:
			x, y, z = pixList[n]
			if(valIndex >= byteNum):
				if(not silent):
					print("\n" + str(byteNum) + " bytes retrieved.")
				break
			if(xthPattern(n, xth)):
				#Extract data from a pixel
				baseColor = averageColor(pixList[n - 1], pixList[n + 1])
				dataColor = retrieveDataColorBaseX((x, y, z), baseColor, 7)
				data = colorTupleBaseXToVal(dataColor, 7)
				f.append(data)
				valIndex += 1
				if(not silent):
					sys.stdout.write("\r" + str(int((valIndex/byteNum) * 100)) + "% Complete")
					sys.stdout.flush()
			else:
				pass
		except:
			print("\nERROR: Could not retrieve bytes.")
			print(str(valIndex) + "/" + str(byteNum) + " bytes retrieved before Error.")
			os._exit()
	return f
	
#####################################################
def inColorInject(args = None): #args should be [pixList, newPixList, intFiList, [Relevant CLI Args as list]]
	pixList = args[0]
	newPixList = args[1]
	intFiList = args[2]
	color = args[3][0] #The only arg this accepts is X
	dist = int(args[3][1])
	valIndex = 0
	byteNum = len(intFiList)
	for n in range(4, len(pixList) - 1):
		x, y, z = pixList[n]
		baseColor = averageColor(pixList[n - 1], pixList[n + 1])
		if(inColorPattern(n, baseColor, [color, dist])):
			#Write the data to a pixel
			if(valIndex < len(intFiList)):
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
	return newPixList

def inColorRetrieve(args = None, silent = False):#args should be [pixList, byteNum, [Relevant CLI Args as list]]
	pixList = args[0]
	byteNum = args[1]
	color = args[2][0]
	dist = args[2][1]
	f = []
	valIndex = 0
	for n in range(4, len(pixList) - 1):
		try:
			x, y, z = pixList[n]
			baseColor = averageColor(pixList[n - 1], pixList[n + 1])
			if(valIndex >= byteNum):
				if(not silent):
					print("\n" + str(byteNum) + " bytes retrieved.")
				break
			if(inColorPattern(n, baseColor, [color, dist])):
				#Extract data from a pixel
				dataColor = retrieveDataColorBaseX((x, y, z), baseColor, 7)
				data = colorTupleBaseXToVal(dataColor, 7)
				f.append(data)
				valIndex += 1
				if(not silent):
					sys.stdout.write("\r" + str(int((valIndex/byteNum) * 100)) + "% Complete")
					sys.stdout.flush()
			else:
				pass
		except:
			print("\nERROR: Could not retrieve bytes.")
			print(str(valIndex) + "/" + str(byteNum) + " bytes retrieved before Error.")
			os._exit(1)
	return f