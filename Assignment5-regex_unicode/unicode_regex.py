import re

inp = input("Enter the input text: ") 
allChar = re.compile('[^\W_]', re.IGNORECASE | re.UNICODE)

if re.match(allChar, inp):
	print("The input is Unicode text")
else:
	print("You have not entered unicode text")
