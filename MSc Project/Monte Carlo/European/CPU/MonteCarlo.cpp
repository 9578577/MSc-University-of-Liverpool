/*
 * Matthew Carter - University of Liverpool
 * Least Squares Monte Carlo for European Option
 */

#include "MonteCarlo.h"

DATA_TYPE standard_error;

DATA_TYPE monte_carlo(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE D, DATA_TYPE r, DATA_TYPE v, int type, int M, int N) {
    MTRand rand = seedRand(S);

    // Compute constants
    DATA_TYPE deltaT = T / (DATA_TYPE)N;
    DATA_TYPE nudt = (r - D - 0.5 * v * v) * deltaT; 
    DATA_TYPE vdt = v * sqrt(deltaT);
    DATA_TYPE disc = exp(-r * T);

    DATA_TYPE sum_CT = 0;
    DATA_TYPE sum_CT2 = 0;

    DATA_TYPE *S_T = (DATA_TYPE *)malloc(M * N * sizeof(DATA_TYPE));

    struct timeval stop, start;

    // Set initial stock price for M paths
    for(int i = 0; i < M; i++) {
        S_T[i * N] = S;
    }

    // Generate M paths with N steps
    for(int i = 0; i < M; i++) {
        for(int j = 1; j < N; j++) {
            // Generate two uniformly distributed random numbers
            DATA_TYPE x1 = ((DATA_TYPE)genRandLong(&rand) / (unsigned long)0xffffffff);
            DATA_TYPE x2 = ((DATA_TYPE)genRandLong(&rand) / (unsigned long)0xffffffff);

            // Transform to normal distribution
            DATA_TYPE eps = box_muller(x1, x2);

            // Take step
            S_T[i * N + j] = S_T[i * N + (j-1)] * exp(nudt + vdt * eps);
        }
    }

    // Determine option price
    for(int i = 0; i < M; i++) {
        if (type == 0) {
            // Call price
            S_T[i * N + (N-1)] = max(S_T[i * N + (N-1)] - K, 0);
        } else {
            // Put price
            S_T[i * N + (N-1)] = max(K - S_T[i * N + (N-1)], 0);
        }
    }

    // Sums for value, standard deviation and standard error
    for(int i = 0; i < M; i++) {
        sum_CT += S_T[i * N + (N-1)];
        sum_CT2 += S_T[i * N + (N-1)] * S_T[i * N + (N-1)];
    }

    DATA_TYPE value = sum_CT / (DATA_TYPE)M * disc; // Calculate value of option
    DATA_TYPE SD = sqrt((sum_CT2 - (sum_CT * sum_CT) / (DATA_TYPE)M) * exp(-2 * r * T) / ((DATA_TYPE)M - 1)); // Calculate standard deviaton
    standard_error = SD / sqrt(M); // Calculate standard error

    free(S_T);
    return value;
}

int main() {
    OptionData data;
    DATA_TYPE option_price;
    struct timeval stop, start;

    data.S = 50;      // Price of underlying asset ($50)
    data.K = 50;      // Strike price ($50)
    data.r = 0.05;    // Risk-free rate (5%)
    data.v = 0.2;     // Volatility (20%)
    data.T = 1.0;     // Time to maturity
    data.D = 0.0;     // Dividend yield
    data.type = 1;    // 0 = call option, 1 = put option
    data.M = 1000000;    // Number of simulations
    data.N = 100;      // Number of paths per simulation (1 for European option)

    std::cout << "================================" << std::endl;
    std::cout << "=== Black-Scholes Parameters ===" << std::endl;
    std::cout << "================================" << std::endl;
    std::cout << "Price of underlying asset " << data.S << std::endl;
    std::cout << "Strike price " << data.K << std::endl;
    std::cout << "Risk-free rate " << data.r << std::endl;
    std::cout << "Volatility " << data.v << std::endl;
    std::cout << "Time to maturity " << data.T << std::endl;
    std::cout << "================================" << std::endl;
    std::cout << "==== Monte Carlo Parameters ====" << std::endl;
    std::cout << "================================" << std::endl;
    std::cout << "Number of simulated paths " << data.M << std::endl;
    std::cout << "Number of steps per path " << data.N << std::endl;
    std::cout << "================================" << std::endl;
    gettimeofday(&start, NULL);
    option_price = monte_carlo(data.S, data.K, data.T, data.D, data.r, data.v, data.type, data.M, data.N);
    gettimeofday(&stop, NULL);
    std::cout << std::setprecision(8) << "Option price " << option_price << std::endl;
    std::cout << std::setprecision(8) << "Standard error " << standard_error << std::endl;
    std::cout << "================================\n" << std::endl;
    std::cout << std::setprecision(8) << "Execution time: " << (double) (stop.tv_usec - start.tv_usec) / 1000000 + (double) (stop.tv_sec - start.tv_sec) << " seconds" << std::endl;
    std::cout << "================================" << std::endl;

    return 0;
}