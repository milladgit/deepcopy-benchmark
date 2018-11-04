
import os,sys

def generate_classes(class_tmpl, count):
	q = ""
	count -= 1
	r = range(count)
	r = reversed(r)

	q += "class L%d {};\n" % (count)
	for r1 in r:
		q += class_tmpl % ("L%d" % (r1), "L%d" % (r1+1))

	return q


def load_template_file(filename):
	f = open(filename, "r")
	lines = f.readlines()
	f.close()
	return ''.join(lines)


def create_chain_of_pointers(count, init_all_arrays=False):
	ret = ""

	i = 0
	ret += "L%d *a%d = new L%d();\n" % (i, i, i)
	if init_all_arrays:
		ret += "\ta%d->A = new datatype[N];\n" % (i)

	i += 1
	tmpl = "\tL%d *a%d = a%d->Lnext = new L%d();\n"
	while i<count:
		ret += tmpl % (i, i, i-1, i)

		if init_all_arrays and i < count-1:
			ret += "\ta%d->A = new datatype[N];\n" % (i)
		i += 1

	if not init_all_arrays:
		ret += "\ta%d->A = new datatype[N];\n" % (count-2)

	return ret


def create_chain_of_pointers_with_serialize(count, init_all_arrays=False):
	ret = ""

	ret += "size_t sz = 0;\n"

	i = 0
	ret += "sz += sizeof(L%d);\n" % (i)
	if init_all_arrays:
		ret += "sz += sizeof(datatype)*N;\n"

	i += 1
	tmpl = "\tL%d *a%d = a%d->Lnext = new L%d();\n"
	while i<count:
		ret += "sz += sizeof(L%d);\n" % (i)

		if init_all_arrays and i < count-1:
			ret += "sz += sizeof(datatype)*N;\n"
		i += 1

	if not init_all_arrays:
		ret += "sz += sizeof(datatype)*N;\n"


	ret += "\nTransferUnit tu;\ntu.init(sz);\n"



	i = 0
	ret += "L%d *a%d = (L%d*) tu.get_next_ptr(sizeof(L%d));\n" % (i, i, i, i)
	if init_all_arrays or i == count-2:
		ret += "a%d->A = (datatype*) tu.get_next_ptr(sizeof(datatype)*N);\n" % (i)

	i += 1
	tmpl = "\tL%d *a%d = a%d->Lnext = (L%d *) tu.get_next_ptr(sizeof(L%d));\n"
	while i<count:
		ret += tmpl % (i, i, i-1, i, i)

		if i < count-1:
			if init_all_arrays or i == count-2:
				ret += "\ta%d->A = (datatype*) tu.get_next_ptr(sizeof(datatype)*N);\n" % (i)
		# elif count == 2 and i == 1:
		# 	ret += "\ta%d->A = (datatype*) tu.get_next_ptr(sizeof(datatype)*N);\n" % (i-1)
		i += 1

	# if not init_all_arrays:
	# 	ret += "\ta%d->A = (datatype*) tu.get_next_ptr(sizeof(datatype)*N);\n" % (count-2)


	return ret


def init_only_the_last_pointer(count):
	ret = ""
	ret += "for(int i=0;i<N;i++)\n"
	ret += "\t\ta%d->A[i] = i;\n" % (count-2)
	return ret


def generate_chain(count):
	chain = "a0->"
	i = 0
	while i < count-2:
		chain += "Lnext->"
		i += 1
	chain += "A"
	return chain


def generate_compute_code(count, add_pointer_chain_pragmas=False, use_all_arrays=False):
	tmpl = """%s
	#pragma acc parallel loop gang vector present(%s)
	for(int i=0;i<N;i++) {
		%s
	}
	%s
	"""

	pointerchain_declare = ""
	pointerchain_begin = ""
	pointerchain_end   = ""
	computations = ""

	if add_pointer_chain_pragmas:
		pointerchain_begin 	= "#pragma acchelper region begin"
		pointerchain_end	= "#pragma acchelper region end"

	total_var_chain = ""

	if use_all_arrays:
		i = 2
		declare = ""
		while i < count+1:
			var_chain = generate_chain(i)
			total_var_chain += var_chain + ","
			declare += "%s{datatype*}," % (var_chain)
			var = var_chain + "[i] *= scale;\n"
			computations += var
			i += 1
		if len(declare) > 0:
			declare = declare[:-1]

		if add_pointer_chain_pragmas:
			pointerchain_declare = "#pragma acchelper declare(%s) \n\t" % (declare)
	else:
		var_chain = generate_chain(count)
		declare = var_chain
		total_var_chain += var_chain + ","
		if add_pointer_chain_pragmas:
			pointerchain_declare = "#pragma acchelper declare(%s{datatype*}) \n\t" % (declare)
		computations = var_chain + "[i] *= scale;"

	if len(total_var_chain) > 1:
		total_var_chain = total_var_chain[:-1]

	return pointerchain_declare, tmpl % (pointerchain_begin, total_var_chain, computations, pointerchain_end)


def generate_check_results_code_2(count, add_pointer_chain_pragmas=False, use_all_arrays=False):
	tmpl = """
	for(int i=0;i<N;i++) {
		%s
	}
	"""

	computations = ""

	total_var_chain = ""

	if use_all_arrays:
		i = 2
		declare = ""
		while i < count+1:
			var_chain = generate_chain(i)
			total_var_chain += var_chain + ","
			declare += "%s{datatype*}," % (var_chain)
			var = var_chain + "[i] *= scale;\n"
			computations += var
			i += 1
		if len(declare) > 0:
			declare = declare[:-1]

	else:
		var_chain = generate_chain(count)
		declare = var_chain
		total_var_chain += var_chain + ","
		computations = var_chain + "[i] *= scale;"

	if len(total_var_chain) > 1:
		total_var_chain = total_var_chain[:-1]

	return tmpl % (computations)


def generate_check_results_code(count):
	d_var = "datatype *d = %s;" % (generate_chain(count))

	tmpl = """
	for(int i=0;i<N;i++) 
		if(d[i] != i*scale)
			printf("at index: %d\\n", i);
	"""

	ret = "%s%s" % (d_var, tmpl)

	return ret


def generate_transfer_to_gpu_pointerchain(count, init_all_arrays, use_all_arrays):
	ret = ""

	ret += "#pragma acchelper region begin\n"

	L = []
	line = ""

	Lnext = ""
	i = 0
	while i < count-1:
		line = "#pragma acc enter data copyin(a0%s[0:1])\n" % (Lnext)
		L.append(line)
		if init_all_arrays or i == count-2:
			line = "#pragma acc enter data copyin(a0%s->A[0:N])\n" % (Lnext)
			L.append(line)

		Lnext += "->Lnext"
		i += 1

	if use_all_arrays:
		for line in L:
			ret += line
	else:
		if len(L) > 0:
			ret += L[-1]

	ret += "#pragma acchelper region end\n"

	return ret



def generate_transfer_from_gpu_pointerchain(count, init_all_arrays, use_all_arrays):
	ret = ""

	ret += "#pragma acchelper region begin\n"

	L = []
	line = ""

	Lnext = ""
	i = 0
	while i < count-1:
		line = "#pragma acc exit data copyout(a0%s[0:1])\n" % (Lnext)
		L.append(line)
		if init_all_arrays or i == count-2:
			line = "#pragma acc exit data copyout(a0%s->A[0:N])\n" % (Lnext)
			L.append(line)

		Lnext += "->Lnext"
		i += 1

	if use_all_arrays:
		L = reversed(L)
		for line in L:
			ret += line
	else:
		if len(L) > 0:
			ret += L[-1]

	ret += "#pragma acchelper region end\n"

	return ret



def generate_transfer_to_gpu_serialize(count, init_all_arrays):
	ret = ""

	ret += "tu.copyToGPU();\n"

	Lnext = ""
	i = 0
	while i < count-1:
		ret += "acc_attach((void**) &(a0%s));\n" % (Lnext)
		if init_all_arrays or i == count-2:
			ret += "acc_attach((void**) &(a0%s->A));\n" % (Lnext)

		Lnext += "->Lnext"
		i += 1

	return ret



def generate_transfer_from_gpu_serialize(count, init_all_arrays):
	ret = ""

	ret += "tu.copyFromGPU();\n"

	ret += "queue<void*> q2_addr = tu.q_addr;\n"

	Lnext = ""
	i = 0
	while i < count-1:
		ret += "a0%s = (L%d*) tu.get_next_ptr_deserialize(q2_addr);\n" % (Lnext, i)
		if init_all_arrays or i == count-2:
			ret += "a0%s->A = (datatype*) tu.get_next_ptr_deserialize(q2_addr);\n" % (Lnext)

		Lnext += "->Lnext"
		i += 1


	return ret


def generate_transfer_from_gpu_serialize_detach(count, init_all_arrays):
	ret = ""

	Lnext = ""
	i = 0
	while i < count-1:
		ret += "acc_detach((void**) &(a0%s));\n" % (Lnext)
		if init_all_arrays or i == count-2:
			ret += "acc_detach((void**) &(a0%s->A));\n" % (Lnext)

		Lnext += "->Lnext"
		i += 1

	ret += "tu.copyFromGPU();\n"

	return ret



def create_file(count, init_all_arrays, use_all_arrays, with_pointerchain, enable_serialize, output_filename, template_filename):
	class_tmpl = load_template_file("template-class.tmpl")
	class_defs = generate_classes(class_tmpl, count)

	if enable_serialize:
		chain_of_pointers = create_chain_of_pointers_with_serialize(count, init_all_arrays)
	else:
		chain_of_pointers = create_chain_of_pointers(count, init_all_arrays)

	init_only_last = init_only_the_last_pointer(count)

	pointerchain_declare, compute_code = generate_compute_code(count, with_pointerchain, use_all_arrays)

	results_code = generate_check_results_code_2(count, with_pointerchain, use_all_arrays)

	transfer_to_gpu = ""
	transfer_from_gpu = ""

	if with_pointerchain:
		transfer_to_gpu = generate_transfer_to_gpu_pointerchain(count, init_all_arrays, use_all_arrays)
		transfer_from_gpu = generate_transfer_from_gpu_pointerchain(count, init_all_arrays, use_all_arrays)
	elif enable_serialize:
		transfer_to_gpu = generate_transfer_to_gpu_serialize(count, init_all_arrays)
		# transfer_from_gpu = generate_transfer_from_gpu_serialize(count, init_all_arrays)
		transfer_from_gpu = generate_transfer_from_gpu_serialize_detach(count, init_all_arrays)

	if with_pointerchain:
		transfer_to_gpu = pointerchain_declare + "\n\n" + transfer_to_gpu

	main_tmpl = load_template_file(template_filename)
	main_file = main_tmpl % (class_defs, chain_of_pointers, init_only_last, transfer_to_gpu, compute_code, transfer_from_gpu, results_code)

	f = open(output_filename, "w")
	f.write(main_file)
	f.close()


def main():

	count = 5
	init_all_arrays = True
	use_all_arrays = init_all_arrays
	with_pointerchain = True
	enable_serialize = False

	os.system("rm -rf src/")
	os.system("mkdir -p src")
	os.system("rm -rf src-googlebench/")
	os.system("mkdir -p src-googlebench")

	files_generated = 0

	for count in range(2,11):
		for all_init, all_used in [(True, True), (True, False), (False, False)]:

			for approach in ["uvm", "pointerchain", "serialize"]:

				with_pointerchain = False
				enable_serialize = False

				if approach == "pointerchain":
					with_pointerchain = True
				elif approach == "serialize":
					enable_serialize = True

				output_filename = "benchmark-k%d" % (count)
				if all_init:
					output_filename += "-allinit"
				else:
					output_filename += "-LLinit"

				if all_used:
					output_filename += "-allused"
				else:
					output_filename += "-LLused"

				if approach == "uvm":
					output_filename += "-uvm"
				elif approach == "pointerchain":
					output_filename += "-pc"
				elif approach == "serialize":
					output_filename += "-seriz"

				output_filename_final = "./src/" + output_filename + ".cpp"
				create_file(count, all_init, all_used, with_pointerchain, enable_serialize, output_filename_final, "template-main.tmpl")
				output_filename_final = "./src-googlebench/" + output_filename + ".cpp"
				create_file(count, all_init, all_used, with_pointerchain, enable_serialize, output_filename_final, "template-googlebench-main.tmpl")
				files_generated += 1

	print "%s x 2 files were created!" % (files_generated)


if __name__ == '__main__':
	main()
