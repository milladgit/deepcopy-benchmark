
BIN = ./bin
BIN_GOOGLE_BENCH = ./bin-googlebench

all: normal googlebench

normal: $(BIN)/dense_uvm $(BIN)/dense_deepcopy $(BIN)/dense_uvm_selective $(BIN)/dense_deepcopy_selective $(BIN)/dense_pointerchain_selective

$(BIN)/dense_uvm: src/uvm.cpp
	mkdir -p $(BIN)
	pgc++ -w -std=c++11 -O3 -mp -acc -ta=tesla:managed,cc70,cc60 -I. $^ -o $@

$(BIN)/dense_deepcopy: src/deepcopy.cpp
	mkdir -p $(BIN)
	pgc++ -w -std=c++11 -O3 -mp -acc -ta=tesla:cc70,cc60 -I. $^ -o $@

$(BIN)/dense_uvm_selective: src/uvm_selective.cpp
	mkdir -p $(BIN)
	pgc++ -w -std=c++11 -O3 -mp -acc -ta=tesla:managed,cc70,cc60 -I. $^ -o $@

$(BIN)/dense_deepcopy_selective: src/deepcopy_selective.cpp
	mkdir -p $(BIN)
	pgc++ -w -std=c++11 -O3 -mp -acc -ta=tesla:cc70,cc60 -I. $^ -o $@

$(BIN)/dense_pointerchain_selective: src/pointerchain_selective.cpp
	mkdir -p $(BIN)
	pgc++ -w -std=c++11 -O3 -mp -acc -ta=tesla:cc70,cc60 -I. $^ -o $@



googlebench: $(BIN_GOOGLE_BENCH)/dense_uvm $(BIN_GOOGLE_BENCH)/dense_deepcopy $(BIN_GOOGLE_BENCH)/dense_uvm_selective $(BIN_GOOGLE_BENCH)/dense_deepcopy_selective $(BIN_GOOGLE_BENCH)/dense_pointerchain_selective

$(BIN_GOOGLE_BENCH)/dense_uvm: src-googlebench/uvm.cpp
	mkdir -p $(BIN_GOOGLE_BENCH)
	pgc++ -w -std=c++11 -O3 -mp -acc -ta=tesla:managed,cc70,cc60 -I. $^ -o $@

$(BIN_GOOGLE_BENCH)/dense_deepcopy: src-googlebench/deepcopy.cpp
	mkdir -p $(BIN_GOOGLE_BENCH)
	pgc++ -w -std=c++11 -O3 -mp -acc -ta=tesla:cc70,cc60 -I. $^ -o $@

$(BIN_GOOGLE_BENCH)/dense_uvm_selective: src-googlebench/uvm_selective.cpp
	mkdir -p $(BIN_GOOGLE_BENCH)
	pgc++ -w -std=c++11 -O3 -mp -acc -ta=tesla:managed,cc70,cc60 -I. $^ -o $@

$(BIN_GOOGLE_BENCH)/dense_deepcopy_selective: src-googlebench/deepcopy_selective.cpp
	mkdir -p $(BIN_GOOGLE_BENCH)
	pgc++ -w -std=c++11 -O3 -mp -acc -ta=tesla:cc70,cc60 -I. $^ -o $@

$(BIN_GOOGLE_BENCH)/dense_pointerchain_selective: src-googlebench/pointerchain_selective.cpp
	mkdir -p $(BIN_GOOGLE_BENCH)
	pgc++ -w -std=c++11 -O3 -mp -acc -ta=tesla:cc70,cc60 -I. $^ -o $@



.PHONY: clean 

clean:
	rm -rf a.out $(BIN) $(BIN_GOOGLE_BENCH)

