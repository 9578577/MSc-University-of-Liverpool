/*
 * Matthew Carter
 * Black Scholes for European Options
 */

#include "BlackScholes.h"

// Calculate d1 in the Black-Scholes formula
DATA_TYPE d1(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v) {
    return log(S / K) + ((r + 0.5 * v * v) * T) / (v * pow(T, 0.5));
}

// Calculate d2 in the Black-Scholes formula
DATA_TYPE d2(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v) {
    return log(S / K) + ((r - 0.5 * v * v) * T) / (v * pow(T, 0.5));
}

// Calculate the price of a call option
DATA_TYPE call_price(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v) {
    return (S * norm_cdf(d1(S, K, T, r, v))) - (K * exp(-r * T) * norm_cdf(d2(S, K, T, r, v)));
}

// Calculate the price of a put option
DATA_TYPE put_price(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v) {
    return (K * exp(-r * T) * norm_cdf(-d2(S, K, T, r, v))) - (S * norm_cdf(-d1(S, K, T, r, v)));
}

int main() {
    OptionData data;
    DATA_TYPE call, put;

    data.S = 50;      // Price of underlying asset ($50)
    data.K = 50;      // Strike price ($50)
    data.r = 0.05;    // Risk-free rate (5%)
    data.v = 0.2;     // Volatility (20%)
    data.T = 1.0;     // Time to maturity

    printf("================================\n");
    printf("=== Black-Scholes Parameters ===\n");
    printf("Price of underlying asset %.2f\n", data.S);
    printf("Strike price              %.2f\n", data.K);
    printf("Risk-free rate            %.2f\n", data.r);
    printf("Volatility                %.2f\n", data.v);
    printf("Time to maturity          %.2f\n", data.T);
    printf("================================\n");
    printf("Call price               $%.8f\n", call_price(data.S, data.K, data.T, data.r, data.v));
    printf("Put price               $%.8f\n", put_price(data.S, data.K, data.T, data.r, data.v));
    printf("================================\n");


    return 0;
}