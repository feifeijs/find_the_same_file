import hashlib,time,sys


if len(sys.argv) != 2:
	print("Usage: %s <filename_to_digest>" %(sys.argv[0]))
	sys.exit(1)




filename = sys.argv[0]
bsize = 8192

algos=hashlib.algorithms

for algo in algos:
	inst = hashlib.new(algo)
	fh = open(filename)
	t1 = time.time()
	while True:
		block = fh.read(bsize)
		if block == "":
			break
		else:
			inst.update(block)
	hashresult = inst.hexdigest()
	t2 = time.time()
	tdiff = t2 - t1
	print("algo: %s time: %f" % (algo, tdiff))
	fh.close()

