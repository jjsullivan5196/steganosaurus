import io
##useful for making sure everything comes out intact
f1 = str(input("Enter first file name: "))
f2 = str(input("Enter second file name: "))
file1 = io.open(f1, 'rb')
file2 = io.open(f2, 'rb')
bytes1 = list(file1.read())
bytes2 = list(file2.read())
index = 0
for x, y in zip(bytes1, bytes2):
	if(x != y):
		print("Byte #" + str(index) + " is different")
		print(str(x) + " vs " + str(y))
	index += 1