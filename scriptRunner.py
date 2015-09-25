import os
mode = str(input("Inject/Retrieve or Check? (i/r/c): "))
if(mode == "i"):
	image = str(input("Enter name of image file: "))
	file = str(input("Enter name of file to inject: "))
	outImage = str(input("Enter name of output image: "))
	os.system("newAndImproved.py " + image + " " + file + " " + outImage)
elif(mode == "r"):
	image = str(input("Enter name of image file: "))
	if(str(input("Override filename? (y/N): ")) == "y"):
		outFile = str(input("Enter name of output file: "))
	else:
		outFile = ""
	os.system("newAndImprovedReverser.py " + image + " " + outFile)
elif(mode == "c"):
	image = str(input("Enter name of image file: "))
	mode = str(input("Max Bytes or Check for stored image?(m/c): "))
	os.system("imageChecker.py " + image + " " + mode)
else:
	print("Invalid mode, please re-run launcher.")