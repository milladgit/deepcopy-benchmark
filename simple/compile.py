
import os, sys, glob

def appendToFile(filename, content):
	f = open(filename, "a")
	f.write(content + "\n")
	f.close()


def is_integer(value):
	try:
		int(value)
		return True
	except ValueError:
		print "Unable to parse the input!"
		return False


def generate_main_body(main_bench, google_bench):
	ahf="python ~/acchelper/acchelper.py forward"
	ahb="python ~/acchelper/acchelper.py backward"

	google_bench_header 	= "-I%s/benchmark/bin/include/" % (os.environ["HOME"])
	google_bench_lib_path  	= "-L%s/benchmark/bin/lib" % (os.environ["HOME"])
	google_bench_lib 		= "-lbenchmark"

	if main_bench:
		os.system("rm -rf bin")
		os.system("mkdir -p bin")
		os.system("cd src;" + ahf + ";cd ..;")

	if google_bench:
		os.system("rm -rf bin-googlebench")
		os.system("mkdir -p bin-googlebench")
		os.system("cd src-googlebench;" + ahf + ";cd ..;")

	os.system("rm -f log-compile.log")
	os.system("rm -f compile-output.log")

	pattern_list = []

	if main_bench:
		pattern_list.append("src/*.cpp")

	if google_bench:
		pattern_list.append("src-googlebench/*.cpp")


	for pattern in pattern_list:

		filelist = []

		filelist = glob.glob(pattern)

		filelist = sorted(filelist)


		compile_cmd = "pgc++ -std=c++11 -w -O3 -mp -acc -ta=tesla%s %s %s %s -o %s %s >> log-compile.log 2>&1"

		for f in filelist:
			managed = ":cc70,cc60"
			if "uvm" in f:
				managed = ":cc70,cc60,managed"

			last_index_slash = f.rfind('/')
			if last_index_slash == -1:
				last_index_slash = 0

			bin_folder = "bin"
			if "googlebench" in pattern:
				bin_folder = "bin-googlebench"

			output_filename = "./%s/exe_%s" % (bin_folder, f[last_index_slash+len("benchmark-")+1:f.index(".")])
			print "Compiling file: %s" % (f)
			cmd = compile_cmd % (managed, google_bench_header, google_bench_lib_path, f, output_filename, google_bench_lib)
			os.system(cmd)
			appendToFile("compile-output.log", cmd)

	if main_bench:
		os.system("cd src;" + ahb + ";cd ..;")

	if google_bench:
		os.system("cd src-googlebench;" + ahb + ";cd ..;")


	print "Error count:"
	os.system("wc -l log-compile.log")


def main():

	while True:
		print "\n\nWhich source files to generate:"
		print "1- Main source files"
		print "2- Google Benchmark files"
		print "3- Both"
		print "0- Exit"

		inp = raw_input("Your choice: ")
		print "---------"
		if is_integer(inp):
			inp = int(inp)
			if inp == 0:
				break
			elif inp == 1:
				generate_main_body(True, False)
			elif inp == 2:
				generate_main_body(False, True)
			elif inp == 3:
				generate_main_body(True, True)
			else:
				print "Please choose from above options."
				continue
			break



if __name__ == '__main__':
	main()
