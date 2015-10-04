import os, sys

args = sys.argv

###HELP STRINGS###
usage = '''usage: ''' + args[0]
default = usage + ''' [-o X] mode [arguments]

positional arguments:
  -o X     Overrides the algorithm to use every Xth pixel. Default 3
  mode     Program mode to use. Valid modes: inject, retrieve and check.
  
Entering a mode with no arguments will display help for that mode.'''
injHelp = usage + ''' inject image infile outfile

description: Injects the image provided with a file.

positional arguments:
  image       Image to hide file in.
  infile      File to hide in image.
  outfile     Name of final image.'''
retHelp = usage + ''' retrieve image [outputName]

description: Retrieves an injected image from image.

positional arguments:
  image                 Image to retrieve file from.
  outputName            Name of output file (override default)'''
checkHelp = usage + ''' check image

description: Checks an image for injectability and presence of injected files.

positional arguments:
  image       Image to check.'''
###Variable Defaults###
opt = ["-1"]
alg = "xth"
colorOpts = ["black", "white", "red", "green", "blue", "yellow", "orange", "purple"]
colorDict = {"black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0), "orange":(255, 127, 0), "yellow":(255, 255, 0), "green":(0, 255, 0), "blue":(0, 0, 255), "purple": (255, 0, 255)}
#First, read algorithm if possible
if(len(args) >=3):
	if(args[1] == "-a"):
		args.pop(1)
		alg = args.pop(1)
if(alg == "inColor"):
	opt = ["0", "0", "0", "10"]
#Again, make sure there's some command to read
if(len(args) >=3):
	if(args[1] == "-o"):
		if(alg == "xth"):
			opt = []
			args.pop(1)
			opt.append(args.pop(1))
		#There'll eventually be more here
		elif(alg == "inColor"):
			opt = []
			args.pop(1)
			if(args[1] in colorOpts):
				opt.append(str(colorDict[args[1]][0]))
				opt.append(str(colorDict[args[1]][1]))
				opt.append(str(colorDict[args[1]][2]))
				args.pop(1)
			else:
				opt.append(args.pop(1)) #R
				opt.append(args.pop(1)) #G
				opt.append(args.pop(1)) #B
			try:
				int(args[1])
				opt.append(args.pop(1)) #Dist
			except:
				opt.append("10")
			try:
				for x in opt:
					int(x)
			except:
				print("Malformed Options, use -o R G B distance")
				os._exit(1)
algArg = ""
for x in opt:
	algArg += x + " "
algArg += alg
###LOGIC###
if(len(args) == 1):
	print(default)
	os._exit(1)
#Non-options mode
if(args[1] == "inject"):
	if(len(args) == 2):
		print(injHelp)
	elif(len(args) != 5):
		print("Invalid number of arguments. Type 'py " + args[0] + " inject' for help")
	else:
		os.system("checker.py \"" + args[1] + "\" \"" + args[2] + "\" \"" + args[3] + "\" \"" + args[4] + "\" " + algArg)
elif(args[1] == "retrieve"):
	if(len(args) == 2):
		print(retHelp)
	elif(len(args) > 4):
		print("Invalid number of arguments. Type 'py " + args[0] + " retrieve' for help")
	elif(len(args) == 3):
		os.system("checker.py \"" + args[1] + "\" \"" + args[2] + "\" " + algArg)
	else:
		os.system("checker.py \"" + args[1] + "\" \"" + args[2] + "\" \"" + args[3] + "\" " + algArg)
elif(args[1] == "check"):
	if(len(args) == 2):
		print(checkHelp)
	elif(len(args) != 3):
		print("Invalid number of arguments. Type 'py " + args[0] + " check' for help")
	else:
		os.system("checker.py \"" + args[1] + "\" \"" + args[2] + "\" " + algArg)
else:
	print("Invalid Mode.")
	print(default)