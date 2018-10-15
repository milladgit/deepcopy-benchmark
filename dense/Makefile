
BIN = ./bin


all: $(BIN)/dense_uvm $(BIN)/dense_deepcopy $(BIN)/dense_uvm_selective $(BIN)/dense_deepcopy_selective $(BIN)/dense_pointerchain_selective

$(BIN)/dense_uvm: uvm.cpp
	mkdir -p $(BIN)
	pgc++ -w -std=c++11 -mp -acc -ta=tesla:managed uvm.cpp -o $@

$(BIN)/dense_deepcopy: deepcopy.cpp
	mkdir -p $(BIN)
	pgc++ -w -std=c++11 -mp -acc -ta=tesla deepcopy.cpp -o $(BIN)/dense_deepcopy

$(BIN)/dense_uvm_selective: uvm_selective.cpp
	mkdir -p $(BIN)
	pgc++ -w -std=c++11 -mp -acc -ta=tesla:managed uvm_selective.cpp -o $(BIN)/dense_uvm_selective

$(BIN)/dense_deepcopy_selective: deepcopy_selective.cpp
	mkdir -p $(BIN)
	pgc++ -w -std=c++11 -mp -acc -ta=tesla deepcopy_selective.cpp -o $(BIN)/dense_deepcopy_selective

$(BIN)/dense_pointerchain_selective: pointerchain_selective.cpp
	mkdir -p $(BIN)
	pgc++ -w -std=c++11 -mp -acc -ta=tesla pointerchain_selective.cpp -o $(BIN)/dense_pointerchain_selective




.PHONY: clean 

clean:
	rm -rf a.out $(BIN)

