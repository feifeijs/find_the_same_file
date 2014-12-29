#!/usr/bin/env python

import sys,exifread,operator

def build_JPG_dt_db(JPG_file_list, jpg_dt_db):
	file2tag_dict = {}
	flistfh = open(JPG_file_list)
	for jpgf in flistfh:
		jpgf = jpgf.strip()
		dtresult = JPG_dt_tag(jpgf)
		if dtresult != ':':
			file2tag_dict[jpgf] = dtresult
	flistfh.close()
	sorted_files = sorted(file2tag_dict.items(), key = operator.itemgetter(1))
	jpg_dt_db_fh = open(jpg_dt_db, 'w')
	prev_dtresult = ''
	prev_jpgf = ''
	first_jpgf = ''
	for (jpgf, dtresult) in sorted_files:
		jpg_dt_db_fh.write("%s %s\n" %(dtresult, jpgf))
		if dtresult == prev_dtresult:
			print "%s ==> %s" % (jpgf,first_jpgf)
		else:
			first_jpgf = jpgf
		prev_dtresult = dtresult
		prev_jpgf = jpgf
	jpg_dt_db_fh.close()

def JPG_dt_tag(jpgf):
	jpgfh = open(jpgf, 'rb')
	tags = exifread.process_file(jpgfh)
	dttag = 'EXIF DateTimeOriginal'
	dtsubtag = 'EXIF SubSecTimeOriginal'
	dtvalue = ''
	dtsubvalue = ''
	if dttag in tags:
		dtvalue = str(tags[dttag])
	if dtsubtag in tags:
		dtsubvalue = str(tags[dtsubtag])
	jpgfh.close()
	return dtvalue + ':' + dtsubvalue

def main():
	if len(sys.argv) != 3:
		print("Usage: %s <JPG_file_list> <jpg_dt_db>" % sys.argv[0])
		print("find <abs_file_path_for_jpg_dir> -iname \"jpg\" -type f > JPG_file_list")
		sys.exit(1)
	JPG_file_list = sys.argv[1]
	jpg_dt_db = sys.argv[2]
	build_JPG_dt_db(JPG_file_list, jpg_dt_db)
	
if __name__ == '__main__':
	main()
