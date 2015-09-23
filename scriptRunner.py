import os
mode = str(input("Inject or Retrieve? (i/r)"))
if(mode == "i"):
	image = str(input("Enter name of image file: "))
	file = str(input("Enter name of file to inject: "))
	outImage = str(input("Enter name of output image: "))
	os.system("newAndImproved.py " + image + " " + file + " " + outImage)
elif(mode == "r"):
	image = str(input("Enter name of image file: "))
	outFile = str(input("Enter name of output file: "))
	os.system("newAndImprovedReverser.py " + image + " " + outFile)
else:
	print("Invalid mode, please re-run launcher.")