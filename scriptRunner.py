import os
mode = str(input("Inject/Retrieve or Check? (i/r/c): "))
if(mode == "i"):
	image = str(input("Enter name of image file: "))
	file = str(input("Enter name of file to inject: "))
	outImage = str(input("Enter name of output image: "))
	os.system("injector.py " + image + " " + file + " " + outImage)
elif(mode == "r"):
	image = str(input("Enter name of image file: "))
	if(str(input("Override filename? (y/N): ")) == "y"):
		outFile = str(input("Enter name of output file: "))
	else:
		outFile = ""
	os.system("retriever.py " + image + " " + outFile)
elif(mode == "c"):
	image = str(input("Enter name of image file: "))
	os.system("imageChecker.py " + image)
else:
	print("Invalid mode, please re-run launcher.")