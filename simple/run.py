
import os,sys

# iteration_datasize_dict = dict()

# iteration_datasize_dict[1] = 100
# iteration_datasize_dict[10] = 100
# iteration_datasize_dict[100] = 100
# iteration_datasize_dict[1000] = 100
# iteration_datasize_dict[10000] = 50
# iteration_datasize_dict[100000] = 50
# iteration_datasize_dict[1000000] = 50
# iteration_datasize_dict[10000000] = 30
# iteration_datasize_dict[100000000] = 30
# iteration_datasize_dict[1000000000] = 30


filename_pattern = "exe_benchmark-c%d-%s-%s"	# exe_benchmark-c10-allinit-allused-pc

bin_folder="./bin"
output_folder_pattern="./output-n%d"



def usage():
	print "Usage: %s <K> <N> <iter_count>"
	exit(1)

def main():
	if len(sys.argv) < 4:
		usage()

	k = int(sys.argv[1])
	n = int(sys.argv[2])
	iter_count = int(sys.argv[3])

	output_folder = output_folder_pattern % (n)
	os.system("rm -rf %s" % (output_folder))
	os.system("mkdir -p %s" % (output_folder))

	for how_to_initialize in ["allinit-allused", "allinit-LLused", "LLinit-LLused"]:
		for method in ["pc", "seriz", "uvm"]:

			filename_raw = filename_pattern % (k, how_to_initialize, method)

			filename = bin_folder + "/" + filename_raw

			output_filename = output_folder + "/" + (filename_raw[4:])

			os.system("rm -f %s" % (output_filename))

			for i in range(iter_count):
				os.system("%s %d >> %s" % (filename, n, output_filename))





if __name__ == '__main__':
	main()

