
import os, sys, glob

def appendToFile(filename, content):
	f = open(filename, "a")
	f.write(content + "\n")
	f.close()

def main():
	ahf="python ~/acchelper/acchelper.py forward"
	ahb="python ~/acchelper/acchelper.py backward"

	google_bench_header 	= "-I/home/millad/benchmark/bin/include/"
	google_bench_lib_path  	= "-L/home/millad/benchmark/bin/lib"
	google_bench_lib 		= "-lbenchmark"

	os.system("rm -rf bin")
	os.system("rm -rf bin-googlebench")

	os.system("mkdir -p bin")
	os.system("mkdir -p bin-googlebench")

	os.system("cd src;" + ahf + ";cd ..;")
	os.system("cd src-googlebench;" + ahf + ";cd ..;")

	os.system("rm -f log-compile.log")
	os.system("rm -f compile-output.log")

	pattern = None
	if len(sys.argv) >= 2:
		pattern = sys.argv[1]

	print "pattern: %s" % (pattern)

	for pattern in ["src/*.cpp", "src-googlebench/*.cpp"]:
	# for pattern in ["src-googlebench/*.cpp"]:

		filelist = []

		# if pattern is None:
		# 	filelist = glob.glob("./src/*.cpp")
		# else:
		filelist = glob.glob(pattern)

		filelist = sorted(filelist)


		compile_cmd = "pgc++ -std=c++11 -w -O3 -mp -acc -ta=tesla%s %s %s %s -o %s %s &>> log-compile.log"

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

	os.system("cd src;" + ahb + ";cd ..;")
	os.system("cd src-googlebench;" + ahb + ";cd ..;")

	print "Error count:"
	os.system("wc -l log-compile.log")



if __name__ == '__main__':
	main()
