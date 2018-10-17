
import os, sys, glob

def main():
	ahf="python ~/acchelper/acchelper.py forward"
	ahb="python ~/acchelper/acchelper.py backward"

	os.system("mkdir -p bin")

	os.system("cd src;" + ahf + ";cd ..;")

	pattern = None
	if len(sys.argv) >= 2:
		pattern = sys.argv[1]

	print "pattern: %s" % (pattern)

	filelist = []

	if pattern is None:
		filelist = glob.glob("./src/*.cpp")
	else:
		filelist = glob.glob(pattern)

	filelist = sorted(filelist)

	os.system("rm -f log-compile.log")

	compile_cmd = "pgc++ -w -O3 -mp -acc -ta=tesla%s %s -o %s &>> log-compile.log"

	for f in filelist:
		managed = ":cc70,cc60"
		if "uvm" in f:
			managed = ":cc70,cc60,managed"

		last_index_slash = f.rfind('/')
		if last_index_slash == -1:
			last_index_slash = 0
		output_filename = "./bin/exe_%s" % (f[last_index_slash+1:f.index(".")-last_index_slash+1])
		print "Compiling file: %s" % (f)
		print "===Compiling command: %s" % (compile_cmd % (managed, f, output_filename))
		os.system(compile_cmd % (managed, f, output_filename))

	os.system("cd src;" + ahb + ";cd ..;")

	print "Error count:"
	os.system("wc -l log-compile.log")

if __name__ == '__main__':
	main()
