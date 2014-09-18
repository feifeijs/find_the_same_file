#!/usr/bin/python

import sys

if len(sys.argv) != 2:
	print("Usage: %s <md5file>" %(sys.argv[0], ))
	sys.exit(1)

md5file = sys.argv[1]
md5fh = open(md5file)

md5_file_dict = dict()

for line in md5fh:
	words = line.split("==>")
	if len(words) < 2:
		print line
		sys.exit(1)
	filename = words[0]
	md5 = words[1]
	if md5 in md5_file_dict:
		print "%s == %s" %(filename, md5_file_dict[md5])
	else:
		md5_file_dict[md5] = filename
md5fh.close()
