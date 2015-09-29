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
x = "-1"
if(len(args) >=3):
	if(args[1] == "-o"):
		#Eventually this will be HUGE override code
		args.pop(1)
		x = args.pop(1)
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
		os.system("checker.py \"" + args[1] + "\" \"" + args[2] + "\" \"" + args[3] + "\" \"" + args[4] + "\" " + x)
elif(args[1] == "retrieve"):
	if(len(args) == 2):
		print(retHelp)
	elif(len(args) > 4):
		print("Invalid number of arguments. Type 'py " + args[0] + " retrieve' for help")
	elif(len(args) == 3):
		os.system("checker.py \"" + args[1] + "\" \"" + args[2] + "\" " + x)
	else:
		os.system("checker.py \"" + args[1] + "\" \"" + args[2] + "\" \"" + args[3] + "\" " + x)
elif(args[1] == "check"):
	if(len(args) == 2):
		print(checkHelp)
	elif(len(args) != 3):
		print("Invalid number of arguments. Type 'py " + args[0] + " check' for help")
	else:
		os.system("checker.py \"" + args[1] + "\" \"" + args[2] + "\" " + x)
else:
	print("Invalid Mode.")
	print(default)