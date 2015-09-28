def matchesPattern(n, extraArgs=None):
	#Simple bool for matching pixels
	#Literally allows for any complexity of function to be externalized here
	#Returns True if pixel is to be written to, false if it isn't
	if(not extraArgs == None):
		X = int(extraArgs)
	else:
		X = 3
	if((n+1)%X==0):
		return True
	return False
def getMaxBytesGivenPattern(size, headerSize, pattern, extraArgs = None):
	s = 0
	for x in range(headerSize, size):
		if(pattern(x, extraArgs)):
			s += 1
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
	##Red Channel
	if(R < spacer):
		R += x
	else:
		R -= spacer
		R += x
	##Green Channel
	if(G < spacer):
		G += y
	else:
		G -= spacer
		G += y
	##Blue Channel
	if(B < spacer):
		B += z
	else:
		B -= spacer
		B += z
	return tuple([R, G, B])
def retrieveDataColorBaseX(finalColor, baseColor, base):
	R, G, B = finalColor
	x, y, z = baseColor
	i, j, k = 0, 0, 0 #Data
	spacer = base - 1
	#Red Channel
	if(x < spacer):
		i = R - x
	else:
		i = R + spacer - x
	#Green Channel
	if(y < spacer):
		j = G - y
	else:
		j = G + spacer - y
	#Blue Channel
	if(z < spacer):
		k = B - z
	else:
		k = B + spacer - z
	return tuple([i, j, k])
def retrieveBaseColor(finalColor, dataColor, base): #used for checker, ugly
	R, G, B = finalColor
	x, y, z = dataColor
	i, j, k = 0, 0, 0 #Data
	spacer = base - 1
	#Red Channel
	if(x == 0):
		i = R + spacer
	elif((R + x - spacer) < spacer):
		i = R - x
	else:
		i = R + spacer - x
	#Green Channel
	if(y == 0):
		j = G + spacer
	elif((G + y - spacer) < spacer):
		j = G - y
	else:
		j = G + spacer - y
	#Blue Channel
	if(z == 0):
		k = B + spacer
	elif((B + z - spacer) < spacer):
		k = B - z
	else:
		k = B + spacer - z
	return tuple([i, j, k])