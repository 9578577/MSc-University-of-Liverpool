/*
 * Matthew Carter
 * Normal (Gaussian) Distribution Header File
 */

#ifndef _NormalDistribution_h
#define _NormalDistribution_h

#include <math.h>

#include "DataType.h"


// Normal cumulative distribution function
// Formula at http://mathworld.wolfram.com/NormalDistribution.html
DATA_TYPE norm_cdf(DATA_TYPE x) {
    return 0.5 * (1 + erf((x - 0) / (1 * exp(0.5*log(2)))));
}

#endif
