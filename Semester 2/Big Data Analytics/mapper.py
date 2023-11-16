#!/usr/bin/python
# import sys because we need to read and write data to STDIN and STDOUT
import sys
# reading entire line from STDIN (standard input)
for line in sys.stdin:
	# to remove leading and trailing whitespace
	line = line.strip()
	# split the line into words
	words = line.split('\n')
	# we are looping over the words array and printing the word
	# with the count of 1 to the STDOUT
	for word in words:
		values = word.split()
# write the results to STDOUT (standard output);
# what we output here will be the input for the
# Reduce step, i.e. the input for reducer.py
		if(len(values)==2):
		   print '%s\t%s' % (values[0], values[1])