#
BIN = ./bin
BIN_GOOGLE_BENCH = ./bin-googlebench
BIN_GOOGLE_BENCH_COMPUTE = ./bin-googlebench-compute

GOOGLE_BENCH_FOLDER = $(HOME)/benchmark/bin
GOOGLE_BENCH_INCLUDE = $(GOOGLE_BENCH_FOLDER)/include
GOOGLE_BENCH_LIB = $(GOOGLE_BENCH_FOLDER)/lib
GOOGLE_BENCH_LIB_FILE = -lbenchmark

# UVM_FLAGS = -w -std=c++11 -O3 -mp -acc -ta=tesla:managed,cc70,cc60 -I. -I$(GOOGLE_BENCH_INCLUDE) -L$(GOOGLE_BENCH_LIB)
# WO_UVM_FLAGS = -w -std=c++11 -O3 -mp -acc -ta=tesla:cc70,cc60 -I. -I$(GOOGLE_BENCH_INCLUDE) -L$(GOOGLE_BENCH_LIB)

UVM_FLAGS = -w -std=c++11 -O3 -mp -acc -ta=keep,tesla:managed,cc70    -I. -I$(GOOGLE_BENCH_INCLUDE) -L$(GOOGLE_BENCH_LIB)
WO_UVM_FLAGS = -w -std=c++11 -O3 -mp -acc -ta=keep,tesla:cc70		  -I. -I$(GOOGLE_BENCH_INCLUDE) -L$(GOOGLE_BENCH_LIB)



all: normal googlebench googlebenchcompute

normal: $(BIN)/dense_uvm $(BIN)/dense_deepcopy $(BIN)/dense_uvm_selective $(BIN)/dense_deepcopy_selective $(BIN)/dense_pointerchain_selective

$(BIN)/dense_uvm: src/uvm.cpp
	mkdir -p $(BIN)
	pgc++ $(UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN)/dense_deepcopy: src/deepcopy.cpp
	mkdir -p $(BIN)
	pgc++ $(WO_UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN)/dense_uvm_selective: src/uvm_selective.cpp
	mkdir -p $(BIN)
	pgc++ $(UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN)/dense_deepcopy_selective: src/deepcopy_selective.cpp
	mkdir -p $(BIN)
	pgc++ $(WO_UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN)/dense_pointerchain_selective: src/pointerchain_selective.cpp
	mkdir -p $(BIN)
	pgc++ $(WO_UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)



googlebench: $(BIN_GOOGLE_BENCH)/dense_uvm $(BIN_GOOGLE_BENCH)/dense_deepcopy $(BIN_GOOGLE_BENCH)/dense_uvm_selective $(BIN_GOOGLE_BENCH)/dense_deepcopy_selective $(BIN_GOOGLE_BENCH)/dense_pointerchain_selective

$(BIN_GOOGLE_BENCH)/dense_uvm: src-googlebench/uvm.cpp
	mkdir -p $(BIN_GOOGLE_BENCH)
	pgc++ $(UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN_GOOGLE_BENCH)/dense_deepcopy: src-googlebench/deepcopy.cpp
	mkdir -p $(BIN_GOOGLE_BENCH)
	pgc++ $(WO_UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN_GOOGLE_BENCH)/dense_uvm_selective: src-googlebench/uvm_selective.cpp
	mkdir -p $(BIN_GOOGLE_BENCH)
	pgc++ $(UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN_GOOGLE_BENCH)/dense_deepcopy_selective: src-googlebench/deepcopy_selective.cpp
	mkdir -p $(BIN_GOOGLE_BENCH)
	pgc++ $(WO_UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN_GOOGLE_BENCH)/dense_pointerchain_selective: src-googlebench/pointerchain_selective.cpp
	mkdir -p $(BIN_GOOGLE_BENCH)
	pgc++ $(WO_UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)



googlebenchcompute: $(BIN_GOOGLE_BENCH_COMPUTE)/dense_uvm $(BIN_GOOGLE_BENCH_COMPUTE)/dense_deepcopy $(BIN_GOOGLE_BENCH_COMPUTE)/dense_uvm_selective $(BIN_GOOGLE_BENCH_COMPUTE)/dense_deepcopy_selective $(BIN_GOOGLE_BENCH_COMPUTE)/dense_pointerchain_selective

$(BIN_GOOGLE_BENCH_COMPUTE)/dense_uvm: src-googlebench-compute/uvm.cpp
	mkdir -p $(BIN_GOOGLE_BENCH_COMPUTE)
	pgc++ $(UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN_GOOGLE_BENCH_COMPUTE)/dense_deepcopy: src-googlebench-compute/deepcopy.cpp
	mkdir -p $(BIN_GOOGLE_BENCH_COMPUTE)
	pgc++ $(WO_UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN_GOOGLE_BENCH_COMPUTE)/dense_uvm_selective: src-googlebench-compute/uvm_selective.cpp
	mkdir -p $(BIN_GOOGLE_BENCH_COMPUTE)
	pgc++ $(UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN_GOOGLE_BENCH_COMPUTE)/dense_deepcopy_selective: src-googlebench-compute/deepcopy_selective.cpp
	mkdir -p $(BIN_GOOGLE_BENCH_COMPUTE)
	pgc++ $(WO_UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)

$(BIN_GOOGLE_BENCH_COMPUTE)/dense_pointerchain_selective: src-googlebench-compute/pointerchain_selective.cpp
	mkdir -p $(BIN_GOOGLE_BENCH_COMPUTE)
	pgc++ $(WO_UVM_FLAGS) $^ -o $@ $(GOOGLE_BENCH_LIB_FILE)




.PHONY: clean 

clean:
	rm -rf a.out $(BIN) $(BIN_GOOGLE_BENCH) $(BIN_GOOGLE_BENCH_COMPUTE) *.ptx *.bin *.gpu

