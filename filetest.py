from __future__ import division
import array
import random


topscores = set(open('topscores.txt').read().split())
print(topscores)
scorelist = []

for singlescore in topscores:
	singlescore_int = int(singlescore)
	array = singlescore_int
	scorelist.append(singlescore_int)

	print(singlescore)
print(array)

max_val = max(scorelist)
min_val = min(scorelist)
med_val = 0

for item in scorelist:
	if (item != max_val and item != min_val):
		med_val = item

print("max: " + str(max_val))
print("min: " + str(min_val))
print("med: " + str(med_val))

if score > min_val:
	scorelist.append(score4)
	scorelist.remove(min_val)

print(scorelist)

file = open("topscores.txt", "r+")
file.truncate(0)
for item in scorelist:
	file.write(str(item) + "\n")
