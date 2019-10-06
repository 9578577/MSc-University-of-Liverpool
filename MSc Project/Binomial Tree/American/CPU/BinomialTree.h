/*
 * Matthew Carter - University of Liverpool
 * Pricing European Options with Binomial Trees
 */

#ifndef _BINIMIALTREE_H
#define _BINIMIALTREE_H

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <iomanip>
#include <math.h>
#include <sys/time.h>

#ifndef max
    #define max(x, y) (((x) > (y)) ? (x) : (y))
#endif

#define MAX_ENTRIES 25
#define MAX_TREE_HEIGHT 30000
#define DATA_TYPE float

DATA_TYPE binomial_tree(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE D, DATA_TYPE r, DATA_TYPE v, int type, int height);

#endif // _BINIMIALTREE_H