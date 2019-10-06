/*
 * Matthew Carter - University of Liverpool
 * Black Scholes Header File
 */

#ifndef _BlackScholes_h
#define _BlackScholes_h

#include <math.h>
#include "DataType.h"
#include "NormalDistribution.h"

DATA_TYPE d1(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v);
DATA_TYPE d2(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v);
DATA_TYPE call_price(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v);
DATA_TYPE put_price(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE r, DATA_TYPE v);

#endif // BlackScholes.h
