#!/usr/bin/python

import hashlib,time,sys,os,os.path
from multiprocessing import Process, Pipe

filepath_arr = []
curproc = 0
proc_arr = []
pconn_arr = []
cconn_arr = []

#main proc code
def main():
	# main proc to find file path, send 10 to cal proc
	# cal proc to cal md5

	global curproc
	global filepath_arr
	global proc_arr
	global pconn_arr
	global cconn_arr

	if len(sys.argv) != 4:
		print("Usage: %s <dir> <n_cal_proc> <result_md5_file>" %(sys.argv[0]))
		sys.exit(1)

	mydir = sys.argv[1]
	n_cal_proc = int(sys.argv[2])
	result_md5_file = sys.argv[3]

	md5fh = open(result_md5_file, "w")
	abspath = os.path.abspath(mydir)
	if not os.path.isdir(abspath):
		print("%s is not a dir" % mydir)
		sys.exit(1)

	#setup cal proc pool
	for i in range(n_cal_proc):
		parent_conn, child_conn = Pipe()
		p = Process(target=cal_md5_loop, args=(child_conn,))
		proc_arr.append(p)
		pconn_arr.append(parent_conn)
		cconn_arr.append(child_conn)
		p.start()
	cal_md5_recursive(abspath, md5fh)

	pconn_arr[0].send(filepath_arr)
	md5results = pconn_arr[0].recv()
	for result in md5results:
		md5fh.write("%s\n" % result)

	for i in range(n_cal_proc):
		pconn_arr[i].send("end_of_cal")
		proc_arr[i].join()

	md5fh.close()

#cal proc code
def cal_md5(abspath):
	bsize = 8192
	md5 = hashlib.md5()
	fh = open(abspath)
	while True:
		block = fh.read(bsize)
		if block == "":
			break
		else:
			md5.update(block)
	hashresult = md5.hexdigest()
	fh.close()
	return hashresult

#cal proc code 
def cal_md5_loop(conn):
	out_arr = []
	while True:
		abs_files = conn.recv()
		if abs_files == "end_of_cal":
			conn.close()
			return
		for absf in abs_files:
			md5 = cal_md5(absf)
			out_arr.append("%s==>%s" % (absf,md5))
		conn.send(out_arr)
		del out_arr[:]

#main proc code
def cal_md5_recursive(absdir, md5fh):
	global curproc
	global pconn_arr
	global filepath_arr

	for e in os.listdir(absdir):
		absfile = os.path.join(absdir, e)
		if os.path.islink(absfile):
			print("Can't process link for %s" % absfile) 
		elif os.path.isfile(absfile):
			filepath_arr.append(absfile)
			if len(filepath_arr) >= 10:
				filepath_arr_send = filepath_arr[0:9]
				del filepath_arr[0:9]
				pconn_arr[curproc].send(filepath_arr_send)
				md5results = pconn_arr[curproc].recv()
				for result in md5results:
					md5fh.write("%s\n" % result)
				curproc = curproc + 1
				if curproc >= len(pconn_arr):
					curproc = 0
		elif os.path.isdir(absfile):
			cal_md5_recursive(absfile, md5fh)
	
if __name__ == "__main__":
	main()
