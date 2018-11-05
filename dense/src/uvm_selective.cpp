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


void do_computation_2(L0 *a0, int N, int Q, datatype scale) {
	int j=Q-1;
	int k=Q-1;
	int t=Q-1;

	#pragma acc parallel loop
	for(int i=0;i<N;i++) 
		a0->Anext[j].Anext[k].Anext[t].A[i] *= scale;

}


void check_results(L0 *a0, int N, int Q, datatype scale) {
	int j=Q-1;
	int k=Q-1;
	int t=Q-1;

	for(int i=0;i<N;i++) {
		if(a0->Anext[j].Anext[k].Anext[t].A[i] != scale*(i+1)) {
			printf("Error in element (%d, %d, %d, %d)\n", j, k, t, i);
		}
	}
}


void show_time(double time, char *topic) {
	if(time >= 0.01) {
		printf("%s - Time: %.2fs\n", topic, time);
	} else {
		time *= 1.0E6;
		printf("%s - Time: %.2fus\n", topic, time);
	}
}


int main(int argc, char const *argv[]) {

	datatype scale = 37;
	int N = 4000;
	int Q = 20;
	if(argc < 3) {
		printf("Usage: %s <N> <Q>\n", argv[0]);
		exit(0);
	}
	N = atoi(argv[1]);
	Q = atoi(argv[2]);

	double time, total_time;
	total_time = omp_get_wtime();


	time = omp_get_wtime();
	L0 *a0 = build_the_structure(N, Q);
	time = omp_get_wtime() - time;
	show_time(time, "Allocation");

	show_time(0, "Transfer to GPU");

	time = omp_get_wtime();
	// do_computation_with_uvm(a0, N, Q, scale);
	do_computation_2(a0, N, Q, scale);
	time = omp_get_wtime() - time;
	show_time(time, "Compute");

	show_time(0, "Transfer from GPU");

	time = omp_get_wtime();
	check_results(a0, N, Q, scale);
	time = omp_get_wtime() - time;
	show_time(time, "Check results");

	total_time = omp_get_wtime() - total_time;
	show_time(total_time, "Total time");

	return 0;
}
