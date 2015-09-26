import io, sys
##useful for making sure everything comes out intact

args = sys.argv

if(len(args) == 1):
	print("usage: py " + args[0] + " file1 file2")
	exit()
if(len(args) == 2):
	print("usage: py " + args[0] + " file1 file2")
	exit()
file1 = io.open(args[1], 'rb')
file2 = io.open(args[2], 'rb')
bytes1 = list(file1.read())
bytes2 = list(file2.read())
index = 0
same = True
for x, y in zip(bytes1, bytes2):
	if(x != y):
		print("Byte #" + str(index) + " is different")
		print(str(x) + " vs " + str(y))
		same = False
	index += 1
if(same):
	print("Files are identical")