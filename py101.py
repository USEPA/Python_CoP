# Sharon D. Kenny
# kenny.sharon@epa.gov
# EPA Region 3
# 215-814-3417

# SECTION 1
import os
import re

yy = os.getcwd()
print (yy)

# SECTION 2

fd = 'gis_rocks.txt'
file = open (fd, 'w')
file.write(
'''
hello world
I am happy@epa.gov
Today is Wednesday\n17 April 2018
''')
file.close()

print ("****************")
fileW = open (fd, 'r')
text = fileW.read()
print(text)
print ("****************")


# SECTION 3


# Let's find all the lines that have 
# a word starting with the letter h
fileW = open(fd)
for line in fileW:
	line = line.rstrip()
	if re.findall('^h', line):
		print(line)