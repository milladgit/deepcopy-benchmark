
import os,sys


bin_folder="./bin"
output_folder = "./output"

app_list = ["dense_uvm", "dense_deepcopy", "dense_uvm_selective", "dense_deepcopy_selective", "dense_pointerchain_selective"]


def usage():
	print "Usage: %s <K> <N> <iter_count>" % (sys.argv[0])
	exit(1)


def main():
	if len(sys.argv) < 4:
		usage()

	k = int(sys.argv[1])
	n = int(sys.argv[2])
	iter_count = int(sys.argv[3])

	# output_folder = output_folder_pattern % (n)
	# os.system("rm -rf %s" % (output_folder))
	os.system("mkdir -p %s" % (output_folder))


	for app in app_list:
		filename = bin_folder + "/" + app
		output_filename = output_folder + "/" + "%s-k%d-n%d" % (app, k, n)
		#os.system("rm -f %s" % (output_filename))
		if os.path.isfile(output_filename):
			continue
		for i in range(iter_count):
			os.system("%s %d %d >> %s" % (filename, n, k, output_filename))


if __name__ == '__main__':
	main()

