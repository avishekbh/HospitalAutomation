from glob import glob
import os

hosp='so'
files_list = glob(os.path.join('./', '*.csv'))
for a_file in sorted(files_list):

	if "peerless" in a_file:
		hosp="peerless"
	# open csv file
	with open(a_file, 'rb') as csvfile:

    	# get number of columns
	    	for line in csvfile.readlines():
    		    array = line.split(',')
    		    for a in array:
        			if a is "#":
        				print "Accepted"
