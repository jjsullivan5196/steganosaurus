def xthPattern(n, xth = 3):
	#Simple bool for matching pixels
	#Literally allows for any complexity of function to be externalized here
	#Returns True if pixel is to be written to, false if it isn't
	if((n+1)%xth==0):
		return True
	return False
def inColorPattern(n, avgColor, otherData = [(0, 0, 0), 10]):
	#Simple bool for matching pixels
	#Literally allows for any complexity of function to be externalized here
	#Returns True if pixel is to be written to, false if it isn't
	targetColor = otherData[0]
	distance = otherData[1]
	if((n%2 == 0) and (avgColor[0] in range(targetColor[0] - distance, targetColor[0] + distance + 1)) and (avgColor[1] in range(targetColor[1] - distance, targetColor[1] + distance + 1)) and (avgColor[2] in range(targetColor[2] - distance, targetColor[2] + distance + 1))):
		return True
	return False
def getMaxBytesGivenPattern(size, headerSize, pattern, extraArgs = None):
	s = 0
	for x in range(headerSize, size):
		if(pattern(x, extraArgs)):
			s += 1
	return s
def getMaxBytesGivenColor(size, pixList, headerSize, pattern, extraArgs = None):
	s = 0
	for x in range(headerSize, size):
		try:
			baseColor = averageColor(pixList[x - 1], pixList[x + 1])
			if(pattern(x, baseColor, extraArgs)):
				s += 1
		except:
			break
	return s
##Used for easy color changing
def averageColor(c1, c2):
	R = int((c1[0] + c2[0])/2)
	G = int((c1[1] + c2[1])/2)
	B = int((c1[2] + c2[2])/2)
	return (R, G, B)
#########################
##GENERALIZED FUNCTIONS##
#########################
def colorTupleFromValue(val, base):
	if(val > (pow(base, 3) - 1)):
		raise Exception("Cannot represent number " + str(val) + " as a 3 digit integer of base " + str(base))
		#You screwed it up
	color = [0, 0, 0]
	
	hundreds = (val - (val%pow(base, 2)))/pow(base, 2)
	color[2] = int(hundreds)
	val -= hundreds * pow(base, 2)
	
	tens = (val - (val%base))/base
	color[1] = int(tens)
	val -= tens * base
	
	color[0] = int(val)
	
	return tuple(color)
def colorTupleBaseXToVal(colorTuple, base):
	return (colorTuple[0] + (colorTuple[1] * base) + (colorTuple[2] * pow(base, 2)))
def injectDataColorBaseX(baseColor, dataColor, base):
	R, G, B = baseColor
	x, y, z = dataColor
	spacer = base - 1
	
	R = (R + x) if (R < spacer) else ((R - spacer) + x) #Red Channel
	G = (G + y) if (G < spacer) else ((G - spacer) + y) #Green Channel
	B = (B + z) if (B < spacer) else ((B - spacer) + z) #Blue Channel
	
	return tuple([R, G, B])
def retrieveDataColorBaseX(finalColor, baseColor, base):
	R, G, B = finalColor
	x, y, z = baseColor
	i, j, k = 0, 0, 0 #Data
	spacer = base - 1
	
	i = (R - x) if (x < spacer) else (R + spacer - x) #Red Channel
	j = (G - y) if (y < spacer) else (G + spacer - y) #Green Channel
	k = (B - z) if (z < spacer) else (B + spacer - z) #Blue Channel
	
	return tuple([i, j, k])
def retrieveBaseColor(finalColor, dataColor, base): #used for checker, ugly
	R, G, B = finalColor
	x, y, z = dataColor
	i, j, k = 0, 0, 0 #Data
	spacer = base - 1
	#Red Channel
	if(x == 0):
		if(R - x > spacer):
			i = R + spacer
		else:
			i = R
	elif((R + x - spacer) < spacer):
		i = R - x
	else:
		i = R + spacer - x
	#Green Channel
	if(y == 0):
		if(G - j > spacer):
			j = G + spacer
		else:
			j = G
	elif((G + y - spacer) < spacer):
		j = G - y
	else:
		j = G + spacer - y
	#Blue Channel
	if(z == 0):
		if(B - k > spacer):
			k = B + spacer
		else:
			k = B
	elif((B + z - spacer) < spacer):
		k = B - z
	else:
		k = B + spacer - z
	return tuple([i, j, k])