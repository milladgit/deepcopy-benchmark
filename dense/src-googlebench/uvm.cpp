#include <stdio.h>
#include <openacc.h>
#include <omp.h>
#include "../datadefs.h"



class L3 {
public:
	datatype 	*A;
	int 		nA;
};

class L2 {
public:
	datatype 	*A;
	int 		nA;
	L3			*Anext;
	int 		nAnext;

	// L2(int N, int Q) {
	// 	A = new datatype[N];
	// 	Anext = new L3[Q];
	// }
};

class L1 {
public:
	datatype 	*A;
	int 		nA;
	L2			*Anext;
	int 		nAnext;

	// L1(int N, int Q) {
	// 	A = new datatype[N];
	// 	Anext = new L2[Q];
	// }
};

class L0 {
public:
	datatype 	*A;
	int 		nA;
	L1			*Anext;
	int 		nAnext;

	// L0(int N, int Q) {
	// 	A = new datatype[N];
	// 	Anext = new L1[Q];
	// }
};



L0 *build_the_structure(int N, int Q) {
	L0 *a0 = new L0();
	a0->A = new datatype[N];
	a0->Anext = new L1[Q];

	for(int i=0;i<Q;i++) {
		a0->Anext[i].A = new datatype[N];
		a0->Anext[i].Anext = new L2[Q];

		for(int j=0;j<Q;j++) {
			a0->Anext[i].Anext[j].A = new datatype[N];
			a0->Anext[i].Anext[j].Anext = new L3[Q];

			for(int k=0;k<Q;k++) {
				a0->Anext[i].Anext[j].Anext[k].A = new datatype[N];

				for(int t=0;t<N;t++) {
					a0->Anext[i].Anext[j].Anext[k].A[t] = t+1;
				}
			}
		}
	}
	return a0;
}

// void do_computation_with_uvm(L0 *a0, int N, int Q, datatype scale) {
// 	#pragma acc parallel loop
// 	for(int i=0;i<N;i++) {
// 		a0->A[i] *= scale;

// 		for(int j=0;j<Q;j++) {
// 			a0->Anext[j].A[i] *= scale;

// 			for(int k=0;k<Q;k++) {
// 				a0->Anext[j].Anext[k].A[i] *= scale;

// 				for(int t=0;t<Q;t++) {
// 					a0->Anext[j].Anext[k].Anext[t].A[i] *= scale;
// 				}
// 			}
// 		}
// 	}

// }


void do_computation_with_uvm_2(L0 *a0, int N, int Q, datatype scale) {
	#pragma acc parallel loop
	for(int i=0;i<N;i++) 
		a0->A[i] *= scale;

	#pragma acc parallel loop
	for(int j=0;j<Q;j++) 
		for(int i=0;i<N;i++)
			a0->Anext[j].A[i] *= scale;

	#pragma acc parallel loop
	for(int j=0;j<Q;j++) 
		for(int k=0;k<Q;k++) 
			for(int i=0;i<N;i++) 
				a0->Anext[j].Anext[k].A[i] *= scale;

	#pragma acc parallel loop
	for(int j=0;j<Q;j++) 
		for(int k=0;k<Q;k++) 
			for(int t=0;t<Q;t++) 
				for(int i=0;i<N;i++) 
					a0->Anext[j].Anext[k].Anext[t].A[i] *= scale;


}


void check_results(L0 *a0, int N, int Q, datatype scale) {
	for(int i=0;i<N;i++) 
		a0->A[i] *= scale;

	for(int j=0;j<Q;j++) 
		for(int i=0;i<N;i++)
			a0->Anext[j].A[i] *= scale;

	for(int j=0;j<Q;j++) 
		for(int k=0;k<Q;k++) 
			for(int i=0;i<N;i++) 
				a0->Anext[j].Anext[k].A[i] *= scale;

	for(int j=0;j<Q;j++) 
		for(int k=0;k<Q;k++) 
			for(int t=0;t<Q;t++) 
				for(int i=0;i<N;i++) 
					a0->Anext[j].Anext[k].Anext[t].A[i] *= scale;

}


void show_time(double time, char *topic) {
	if(time >= 0.01) {
		printf("%s - Time: %.2fs\n", topic, time);
	} else {
		time *= 1.0E6;
		printf("%s - Time: %.2fus\n", topic, time);
	}
}


int deepcopy_body(benchmark::State& state) {

	int N = state.range(0);
	int Q = state.range(1);

	datatype scale = 37;

	L0 *a0 = build_the_structure(N, Q);

	// do_computation_with_uvm(a0, N, Q, scale);
	do_computation_with_uvm_2(a0, N, Q, scale);

	check_results(a0, N, Q, scale);

	return 0;
}



static void BM_Deepcopy(benchmark::State& state) {
	for (auto _ : state)
		deepcopy_body(state);
}
static void CustomArguments(benchmark::internal::Benchmark* b) {

	for(int n=10000;n<=5120000;n*=2)
		for(int q=4;q<=64;q*=2)
			b->Args({n, q});

}
BENCHMARK(BM_Deepcopy)->Apply(CustomArguments);


// BENCHMARK_MAIN();
int main(int argc, char** argv) {
	// for (auto& test_input : { /* ... */ })
	// benchmark::RegisterBenchmark(test_input.name(), BM_test, test_input);

	benchmark::Initialize(&argc, argv);
	benchmark::RunSpecifiedBenchmarks();

	return 0;
}

