#!/usr/bin/env python

import sys,exifread

def main():
	if len(sys.argv) != 2:
		print("Usage: %s <JPG>" % sys.argv[0])
		sys.exit(1)
	JPG = sys.argv[1]
	jpgfh = open(JPG, 'rb')
	tags = exifread.process_file(jpgfh)
	dttag = 'EXIF DateTimeOriginal'
	dtsubtag = 'EXIF SubSecTimeOriginal'
	if dttag in tags:
		print(tags[dttag])
	if dtsubtag in tags:
		print(tags[dtsubtag])
	jpgfh.close()

if __name__ == '__main__':
	main()
