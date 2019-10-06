/*
 * Matthew Carter - University of Liverpool
 * General Addititve Binomial Valuation of European Options
 */

extern "C" {

#include <math.h>

#ifndef max
    #define max(x, y) (((x) > (y)) ? (x) : (y))
#endif

#define MAX_ENTRIES 25
#define MAX_TREE_HEIGHT 30000
#define DATA_TYPE float

DATA_TYPE eu_binomial_tree(DATA_TYPE S,
                           DATA_TYPE K,
                           DATA_TYPE T,
                           DATA_TYPE D,
                           DATA_TYPE r,
                           DATA_TYPE v,
                           int type,
                           int height) {

#pragma HLS inline off

    // Compute starting constants
    DATA_TYPE dt = (float)T / height;
    DATA_TYPE u = 1 + ((r - D) * dt) + (v * sqrt(dt));
    DATA_TYPE d = 1 + ((r - D) * dt) - (v * sqrt(dt));
    DATA_TYPE disc = 1 + (-r * dt);
    DATA_TYPE pu = (1 + ((r - D) * dt) - d) / (u - d);
    DATA_TYPE pd = (1 - pu);
    DATA_TYPE dpu = disc * pu;
    DATA_TYPE dpd = disc * pd;

    DATA_TYPE St[MAX_TREE_HEIGHT];
	#pragma HLS ARRAY_PARTITION variable=St cyclic factor=2 dim=1
    DATA_TYPE temp1[MAX_TREE_HEIGHT];
	#pragma HLS ARRAY_PARTITION variable=temp1 cyclic factor=2 dim=1
    DATA_TYPE temp2[MAX_TREE_HEIGHT];
	#pragma HLS ARRAY_PARTITION variable=temp2 cyclic factor=2 dim=1

    // Determine values from power calculations
    // to be used when initialising assets
    temp1[0] = u;
    temp2[0] = 1;

    power_calculation: for(int i = 1; i < height; i++) {
	#pragma HLS loop_tripcount min=2 max=30000
	#pragma HLS pipeline
	#pragma HLS dependence variable=temp1 inter RAW distance=1 true
	#pragma HLS dependence variable=temp2 inter RAW distance=1 true

    	temp1[i] = temp1[i-1] * u;
    	temp2[i] = temp2[i-1] * d;
    }

    // Tree formation
    if(type == 0) {
    	call_tree_formation: for(int i = 0; i < height; i++) {
		#pragma HLS loop_tripcount min=2 max=30000
		#pragma HLS unroll factor=2
		#pragma HLS pipeline

			St[i] = max((S * temp1[height - i - 1] * temp2[i]) - K, 0);
    	}
    } else {
    	put_tree_formation: for(int i = 0; i < height; i++) {
		#pragma HLS loop_tripcount min=2 max=30000
		#pragma HLS unroll factor=2
		#pragma HLS pipeline

			St[i] = max(K - (S * temp1[height - i - 1] * temp2[i]), 0);
    	}
    }

    // Step back through tree
    loop_traversal_i: for(int i = height-1; i >= 0; i--) {
	#pragma HLS loop_tripcount min=2 max=30000
        loop_traversal_j: for(int j = 0; j <= i; j++) {
		#pragma HLS loop_tripcount min=2 max=30000
		#pragma HLS unroll factor=2
		#pragma HLS pipeline

            St[j] = (dpu * St[j]) + (dpd * St[j+1]);
        }
    }

    return St[0];
}

void binomial_tree(DATA_TYPE *output_r,
                   DATA_TYPE *S,
                   DATA_TYPE *K,
                   DATA_TYPE *T,
                   DATA_TYPE *D,
                   DATA_TYPE *r,
                   DATA_TYPE *v,
                   int *type_r,
                   int *height,
                   int n_options) {
#pragma HLS INTERFACE m_axi port=output_r offset=slave bundle=gmem0
#pragma HLS INTERFACE s_axilite port=output_r bundle=control
#pragma HLS INTERFACE m_axi port=S offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=S bundle=control
#pragma HLS INTERFACE m_axi port=K offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=K bundle=control
#pragma HLS INTERFACE m_axi port=T offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=T bundle=control
#pragma HLS INTERFACE m_axi port=D offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=D bundle=control
#pragma HLS INTERFACE m_axi port=r offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=r bundle=control
#pragma HLS INTERFACE m_axi port=v offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=v bundle=control
#pragma HLS INTERFACE m_axi port=type_r offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=type_r bundle=control
#pragma HLS INTERFACE m_axi port=height offset=slave bundle=gmem1
#pragma HLS INTERFACE s_axilite port=height bundle=control
#pragma HLS INTERFACE s_axilite port=n_options bundle=control
#pragma HLS INTERFACE s_axilite port=return bundle=control

    // Allocate memory on device
    DATA_TYPE temp_output[MAX_ENTRIES];
#pragma HLS ARRAY_PARTITION variable=temp_output cyclic factor=2 dim=1
	DATA_TYPE temp_S[MAX_ENTRIES];
#pragma HLS ARRAY_PARTITION variable=temp_S cyclic factor=2 dim=1
	DATA_TYPE temp_K[MAX_ENTRIES];
#pragma HLS ARRAY_PARTITION variable=temp_K cyclic factor=2 dim=1
	DATA_TYPE temp_T[MAX_ENTRIES];
#pragma HLS ARRAY_PARTITION variable=temp_T cyclic factor=2 dim=1
	DATA_TYPE  temp_D[MAX_ENTRIES];
#pragma HLS ARRAY_PARTITION variable=temp_D cyclic factor=2 dim=1
	DATA_TYPE temp_r[MAX_ENTRIES];
#pragma HLS ARRAY_PARTITION variable=temp_r cyclic factor=2 dim=1
	DATA_TYPE temp_v[MAX_ENTRIES];
#pragma HLS ARRAY_PARTITION variable=temp_v cyclic factor=2 dim=1
    int temp_type[MAX_ENTRIES];
#pragma HLS ARRAY_PARTITION variable=temp_type cyclic factor=2 dim=1
	int temp_height[MAX_ENTRIES];
#pragma HLS ARRAY_PARTITION variable=temp_height cyclic factor=2 dim=1

    // Copy from global to device
    copy_device: for(int i = 0; i < n_options; i++) {
	#pragma HLS loop_tripcount min=1 max=25
	#pragma HLS pipeline
        temp_S[i] = S[i];
        temp_K[i] = K[i];
        temp_T[i] = T[i];
        temp_D[i] = D[i];
        temp_r[i] = r[i];
        temp_v[i] = v[i];
        temp_type[i] = type_r[i];
        temp_height[i] = height[i];
    }

    // Calculate option prices
    price_options: for(int i = 0; i < n_options; i++) {
	#pragma HLS loop_tripcount min=1 max=25
	#pragma HLS unroll factor=2
    	temp_output[i] = eu_binomial_tree(temp_S[i],
										  temp_K[i],
										  temp_T[i],
										  temp_D[i],
										  temp_r[i],
										  temp_v[i],
										  temp_type[i],
										  temp_height[i]);
    }

    // Copy to global memory
    copy_host: for(int i = 0; i < n_options; i++) {
	#pragma HLS loop_tripcount min=1 max=25
	#pragma HLS pipeline
        output_r[i] = temp_output[i];
    }
}

}
