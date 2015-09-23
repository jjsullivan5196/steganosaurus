num = 213
color = [0, 0, 0]
hundreds = (num - (num%49))/49
color[2] = int(hundreds)
num -= hundreds * 49
tens = (num - (num%7))/7
color[1] = int(tens)
num -= tens * 7
color[0] = int(num)	
print(color)
print(color[0] + (color[1] * 7) + (color[2] * 49))