/*
 * Matthew Carter - University of Liverpool
 * Black Scholes Header File
 */

#ifndef _BlackScholes_h
#define _BlackScholes_h

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "../common/DataType.h"
#include "NormalDistribution.h"

// Define data structure to hold option data
typedef struct _OptionData {
    DATA_TYPE S;            // Price of the Underlying Asset
    DATA_TYPE K;            // Strike Price of the Option
    DATA_TYPE r;            // Risk-free Rate
    DATA_TYPE v;            // Volatility of the Underlying Asset
    DATA_TYPE T;            // Time to Expiration in Years
} OptionData;


DATA_TYPE d1(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v);
DATA_TYPE d2(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v);
DATA_TYPE call_price(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v);
DATA_TYPE put_price(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v);

#endif // BlackScholes.h