#include "BlackScholes.h"

// Calculate d1 in the Black-Scholes formula
DATA_TYPE d1(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v) {
    return log(S / K) + ((r + 0.5 * v * v) * T) / (v * exp(0.5*log(T)));
}

// Calculate d2 in the Black-Scholes formula
DATA_TYPE d2(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v) {
    return log(S / K) + ((r - 0.5 * v * v) * T) / (v * exp(0.5*log(T)));
}

// Calculate the price of a call option
DATA_TYPE call_price(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v) {
    return (S * norm_cdf(d1(S, K, T, r, v))) - (K * exp(-r * T) * norm_cdf(d2(S, K, T, r, v)));
}

// Calculate the price of a put option
DATA_TYPE put_price(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v) {
    return (K * exp(-r * T) * norm_cdf(-d2(S, K, T, r, v))) - (S * norm_cdf(-d1(S, K, T, r, v)));
}

void black_scholes(DATA_TYPE *output, DATA_TYPE *S, DATA_TYPE *K, DATA_TYPE *T, DATA_TYPE *r, DATA_TYPE *v) {
#pragma HLS INTERFACE m_axi port=output offset=slave bundle=gmem
#pragma HLS INTERFACE s_axilite port=output bundle=control
#pragma HLS INTERFACE m_axi port=S offset=slave bundle=gmem
#pragma HLS INTERFACE s_axilite port=S bundle=control
#pragma HLS INTERFACE m_axi port=K offset=slave bundle=gmem
#pragma HLS INTERFACE s_axilite port=K bundle=control
#pragma HLS INTERFACE m_axi port=T offset=slave bundle=gmem
#pragma HLS INTERFACE s_axilite port=T bundle=control
#pragma HLS INTERFACE m_axi port=r offset=slave bundle=gmem
#pragma HLS INTERFACE s_axilite port=r bundle=control
#pragma HLS INTERFACE m_axi port=v offset=slave bundle=gmem
#pragma HLS INTERFACE s_axilite port=v bundle=control
#pragma HLS INTERFACE s_axilite port=return bundle=control
#pragma HLS inline region recursive

	DATA_TYPE rate = r[0] /100;
	DATA_TYPE vol = v[0] / 100;

	output[0] = call_price(S[0], K[0], T[0], rate, vol);
	output[1] = put_price(S[0], K[0], T[0], rate, vol);
}
