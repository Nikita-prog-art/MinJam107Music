import os
import pickle
import sys

path = os.path.dirname(os.path.abspath(__file__))

s = "f f fff    ff   fff   ff      fff  ffffff   ff   fff   fff"
s1 = "f f    ffff "

l = []

for c in s1:
	if c == 'f':
		l.append(True)
	else:
		l.append(False)

with open(path + '/pos', 'wb') as file:
	pickle.dump(l, file)
