def matchesPattern(n):
	#Simple bool for matching pixels
	#Literally allows for any complexity of function to be externalized here
	#Returns True if pixel is to be written to, false if it isn't
	if((n+1)%3==0):
		return True
	return False

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
def colorTupleToBaseX(colorTuple, base):
	return (colorTuple[0] + (colorTuple[1] * base) + (colorTuple[2] * pow(base, 2)))
def colorGreaterThan(color, comparison):
	for x in range(len(color)):
		if(color[x] < comparison[x]):
			return False
	return True