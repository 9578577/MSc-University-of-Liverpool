/*
 * Matthew Carter - University of Liverpool
 * Least Squares Monte Carlo for European Option
 * Header file
 */

#ifndef _MonteCarlo_h
#define _MonteCarlo_h

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <iomanip>
#include <math.h>
#include <sys/time.h>

#include "../common/DataType.h"
#include "RNG.h"

#ifndef max
    #define max(x, y) (((x) > (y)) ? (x) : (y))
#endif

// Define data structure to hold option data
typedef struct _OptionData {
    DATA_TYPE S;            // Price of the Underlying Asset
    DATA_TYPE K;            // Strike Price of the Option
    DATA_TYPE r;            // Risk-free Rate
    DATA_TYPE v;            // Volatility of the Underlying Asset
    DATA_TYPE T;            // Time to Expiration in Years
    DATA_TYPE D;            // Dividend yield
    int type;               // Type of option: 0 = call, 1 = put
    int M;                  // Number of simulations
    int N;                  // Number of steps per simulation (1 for EU)
} OptionData;

DATA_TYPE monte_carlo(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE D, DATA_TYPE r, DATA_TYPE v, int type, int M, int N);

#endif // MonteCarlo.h