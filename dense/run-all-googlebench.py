
import os,sys,glob

def usage():
	print "Usage:"
	print "python %s <source_folder> <output_result_folder>" % (sys.argv[0])
	exit(1)

def main():

	if len(sys.argv) < 3:
		usage()

	path = sys.argv[1]
	if path[-1] != "/":
		path += "/"

	output_path = sys.argv[2]
	if output_path[-1] != "/":
		output_path += "/"

	os.system("mkdir -p %s" %(output_path))

	file_list = glob.glob("%s*" % (path))

	if len(file_list) == 0:
		print "No files found at %s" % (path)
		exit(1)

	for filename in file_list:

		app = filename
		output_file = output_path + filename[len(path):]
		cmd = "%s --benchmark_min_time=2 --benchmark_format=csv > %s" % (app, output_file)
		os.system(cmd)




if __name__ == '__main__':
	main()
