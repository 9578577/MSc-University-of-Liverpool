/*
 * Matthew Carter - University of Liverpool
 * Least Squares Monte Carlo for European Option
 *
 * NOTE: Call max(St - K, 0), Put max(K - St, 0)
 */

extern "C" {

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "DataType.h"
#include "RNG.h"

#ifndef max
    #define max(x, y) (((x) > (y)) ? (x) : (y))
#endif

#define MAX_PATHS 1024
#define BURSTBUFFERSIZE 256

DATA_TYPE generate_path(MTRand* rand,
						DATA_TYPE S,
						DATA_TYPE deltaT,
						DATA_TYPE nudt,
						DATA_TYPE vdt,
						int N) {
    DATA_TYPE x1, x2, eps;

    DATA_TYPE path[MAX_PATHS];
	#pragma HLS ARRAY_PARTITION variable=path cyclic factor=2 dim=1

    // Set starting price
    path[0] = S;

    // Take N steps
    take_steps: for(int i = 1; i < N; i++) {
		// Generate two uniformly distributed random numbers
		x1 = ((DATA_TYPE)genRandLong(rand) / (unsigned long)0xffffffff);
		x2 = ((DATA_TYPE)genRandLong(rand) / (unsigned long)0xffffffff);

		// Transform to normal distribution
		eps = box_muller(x1, x2);

		// Take step
        path[i] = path[i-1] * exp(nudt + vdt * eps);
    }

    return path[N-1];
}

void eu_monte_carlo(DATA_TYPE *output_r,
		            DATA_TYPE *S,
					DATA_TYPE *T,
					DATA_TYPE *D,
					DATA_TYPE *r,
					DATA_TYPE *v,
					int M,
					int	N) {
#pragma HLS INTERFACE m_axi port=output_r offset=slave bundle=gmem0
#pragma HLS INTERFACE s_axilite port=output_r bundle=control
#pragma HLS INTERFACE m_axi port=S offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=S bundle=control
#pragma HLS INTERFACE m_axi port=T offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=T bundle=control
#pragma HLS INTERFACE m_axi port=D offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=D bundle=control
#pragma HLS INTERFACE m_axi port=r offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=r bundle=control
#pragma HLS INTERFACE m_axi port=v offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=v bundle=control
#pragma HLS INTERFACE s_axilite port=M bundle=control
#pragma HLS INTERFACE s_axilite port=N bundle=control
#pragma HLS INTERFACE s_axilite port=return bundle=control

	// Seed RNG
	MTRand rand = seedRand(S[0]);

	// Calculate starting constants
    DATA_TYPE deltaT = T[0] / (DATA_TYPE)N;
    DATA_TYPE nudt = (r[0] - D[0] - 0.5 * v[0] * v[0]) * deltaT;
    DATA_TYPE vdt = v[0] * sqrt(deltaT);


    DATA_TYPE burst_buffer[BURSTBUFFERSIZE];

    // Simulate BURSTBUFFERSIZE paths and burst write to memory
    burst_buffer: for(int i = 0; i < M; i += BURSTBUFFERSIZE) {

    	int chunk_size = BURSTBUFFERSIZE;

    	if((i + BURSTBUFFERSIZE) > M) {
    		chunk_size = M - i;
    	}


    	// Generate M paths
    	generate_paths: for(int j = 0; j < chunk_size; j++) {
    		burst_buffer[j] = generate_path(&rand,
    									S[0],
    									deltaT,
    									nudt,
    									vdt,
    									N);
    	}

    	// Burst write to memory
    	write_paths: for(int j = 0; j < chunk_size; j++) {
    		output_r[i + j] = burst_buffer[j];
    	}

    }

}
}
