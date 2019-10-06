/*
 * Matthew Carter - University of Liverpool
 * Black Scholes Header File
 */

#include "NormalDistribution.h"

// Normal probability density function
// Formula at https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.normal.html
DATA_TYPE norm_pdf(DATA_TYPE x, DATA_TYPE mu = 0, DATA_TYPE sigma = 1) {
   return (1 / (pow(2 * M_PI * sigma * sigma, 0.5))) * (exp(-((x - mu) * (x - mu)) / (2 * sigma * sigma)));
}

// Normal cumulative distribution function
// Formula at http://mathworld.wolfram.com/NormalDistribution.html
DATA_TYPE norm_cdf(DATA_TYPE x, DATA_TYPE mu = 0, DATA_TYPE sigma = 1) {
    return 0.5 * (1 + erf((x - mu) / (sigma * pow(2, 0.5))));
}

// Log normal cumulative distribution function
DATA_TYPE norm_log_cdf(DATA_TYPE x, DATA_TYPE mu = 0, DATA_TYPE sigma = 1) {
    return log(norm_cdf(x, mu, sigma));
}