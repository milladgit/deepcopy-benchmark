#include <benchmark/benchmark.h>
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <openacc.h>
#include <queue>
#include "../datadefs.h"

using namespace std;


class TransferUnit {
public:
	char *q;
	size_t q_len;
	size_t total_size;
	char *next_ptr;

	queue<void*> q_addr;

	TransferUnit() {
		q = NULL;
		q_len = 0;
		total_size = 0;
		next_ptr = NULL;		
	}

	void init(size_t sz) {
		q = (char*) malloc(sz);
		next_ptr = q;
		q_len = 0;
		total_size = sz;
	}


	char *get_next_ptr(size_t sz) {
		next_ptr += sz;
		q_len += sz;
		q_addr.push(next_ptr-sz);
		return next_ptr - sz;
	}

	void *get_next_ptr_deserialize(queue<void*> &q_addr_input) {
		void *s = q_addr_input.front();
		q_addr_input.pop();
		return s;
	}

	void copyToGPU() {
		#pragma acc enter data copyin(q[0:total_size])
	}

	void copyFromGPU() {
		#pragma acc exit data copyout(q[0:total_size])		
	}

	void freeMem() {
		free(q);
		q = NULL;
	}

};


class L3 {
public:
	datatype 	*A;
	int 		nA;
};

class L2 {
public:
	datatype 	*A;
	int 		nA;
	L3			*Lnext;
	int 		nLnext;

	// L2(int N, int Q) {
	// 	A = new datatype[N];
	// 	Lnext = new L3[Q];
	// }
};

class L1 {
public:
	datatype 	*A;
	int 		nA;
	L2			*Lnext;
	int 		nLnext;

	// L1(int N, int Q) {
	// 	A = new datatype[N];
	// 	Lnext = new L2[Q];
	// }
};

class L0 {
public:
	datatype 	*A;
	int 		nA;
	L1			*Lnext;
	int 		nLnext;

	// L0(int N, int Q) {
	// 	A = new datatype[N];
	// 	Lnext = new L1[Q];
	// }
};



size_t calculate_size(int N, int Q) {
	size_t sz = 0;
	sz += sizeof(L0);
	sz += sizeof(datatype) * N;
	sz += sizeof(L1) * Q;

	for(int i=0;i<Q;i++) {
		sz += sizeof(datatype) * N;
		sz += sizeof(L2) * Q;

		for(int j=0;j<Q;j++) {
			sz += sizeof(datatype) * N;
			sz += sizeof(L3) * Q;

			for(int k=0;k<Q;k++) {
				sz += sizeof(datatype) * N;
			}
		}
	}
	return sz;
}

L0 *build_the_structure(int N, int Q, TransferUnit &tu) {

	size_t sz = calculate_size(N, Q);

	tu.init(sz);

	L0 *a0 = (L0*) tu.get_next_ptr(sizeof(L0));
	a0->A = (datatype*) tu.get_next_ptr(sizeof(datatype)*N);
	a0->Lnext = (L1*) tu.get_next_ptr(sizeof(L1)*Q);

	for(int i=0;i<Q;i++) {
		a0->Lnext[i].A = (datatype*) tu.get_next_ptr(sizeof(datatype)*N);
		a0->Lnext[i].Lnext = (L2*) tu.get_next_ptr(sizeof(L2)*Q);

		for(int j=0;j<Q;j++) {
			a0->Lnext[i].Lnext[j].A = (datatype*) tu.get_next_ptr(sizeof(datatype)*N);
			a0->Lnext[i].Lnext[j].Lnext = (L3*) tu.get_next_ptr(sizeof(L3)*Q);

			for(int k=0;k<Q;k++) {
				a0->Lnext[i].Lnext[j].Lnext[k].A = (datatype*) tu.get_next_ptr(sizeof(datatype)*N);

				for(int t=0;t<N;t++) {
					a0->Lnext[i].Lnext[j].Lnext[k].A[t] = t+1;
				}
			}
		}
	}

	return a0;
}

void transfer_to_gpu(L0 *a0, int N, int Q, TransferUnit &tu) {
	tu.copyToGPU();
	acc_attach((void**) &(a0));
	// acc_attach((void**) &(a0->A));
	acc_attach((void**) &(a0->Lnext));

	for(int i=0;i<Q;i++) {
		// acc_attach((void**) &(a0->Lnext[i].A));
		acc_attach((void**) &(a0->Lnext[i].Lnext));

		for(int j=0;j<Q;j++) {
			// acc_attach((void**) &(a0->Lnext[i].Lnext[j].A));
			acc_attach((void**) &(a0->Lnext[i].Lnext[j].Lnext));

			for(int k=0;k<Q;k++) {
				acc_attach((void**) &(a0->Lnext[i].Lnext[j].Lnext[k].A));
			}
		}
	}

}



void transfer_to_host(L0 *a0, int N, int Q, TransferUnit &tu) {
	acc_detach((void**) &(a0));
	// acc_detach((void**) &(a0->A));
	acc_detach((void**) &(a0->Lnext));

	for(int i=0;i<Q;i++) {
		// acc_detach((void**) &(a0->Lnext[i].A));
		acc_detach((void**) &(a0->Lnext[i].Lnext));

		for(int j=0;j<Q;j++) {
			// acc_detach((void**) &(a0->Lnext[i].Lnext[j].A));
			acc_detach((void**) &(a0->Lnext[i].Lnext[j].Lnext));

			for(int k=0;k<Q;k++) {
				acc_detach((void**) &(a0->Lnext[i].Lnext[j].Lnext[k].A));
			}
		}
	}
	tu.copyFromGPU();
}

void do_computation(L0 *a0, int N, int Q, datatype scale) {
	// #pragma acc parallel loop present(a0[0:1])
	for(int i=0;i<N;i++) {
		// a0->A[i] *= scale;

		for(int j=0;j<Q;j++) {
			// a0->Lnext[j].A[i] *= scale;

			for(int k=0;k<Q;k++) {
				// a0->Lnext[j].Lnext[k].A[i] *= scale;

				for(int t=0;t<Q;t++) {
					a0->Lnext[j].Lnext[k].Lnext[t].A[i] *= scale;
				}
			}
		}
	}

}


void do_computation_2(L0 *a0, int N, int Q, datatype scale) {
	int j=Q-1;
	int k=Q-1;
	int t=Q-1;

	#pragma acc parallel loop present(a0[0:1])
	for(int i=0;i<N;i++) 
		a0->Lnext[j].Lnext[k].Lnext[t].A[i] *= scale;


}


void check_results(L0 *a0, int N, int Q, datatype scale) {
	int j=Q-1;
	int k=Q-1;
	int t=Q-1;

	for(int i=0;i<N;i++) 
		a0->Lnext[j].Lnext[k].Lnext[t].A[i] *= scale;

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

	TransferUnit tu;

	L0 *a0 = build_the_structure(N, Q, tu);

	transfer_to_gpu(a0, N, Q, tu);

	// do_computation_with_uvm(a0, N, Q, scale);
	do_computation_2(a0, N, Q, scale);

	transfer_to_host(a0, N, Q, tu);

	check_results(a0, N, Q, scale);

	return 0;
}


static void BM_Deepcopy(benchmark::State& state) {
	for (auto _ : state)
		deepcopy_body(state);
}
static void CustomArguments(benchmark::internal::Benchmark* b) {

	for(int n=DENSE_MIN_N;n<=DENSE_MAX_N;n*=DENSE_MUL_N)
		for(int q=DENSE_MIN_Q;q<=DENSE_MAX_Q;q+=DENSE_MUL_Q)
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
