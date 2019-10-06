#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define UPPER_MASK		0x80000000
#define LOWER_MASK		0x7fffffff
#define TEMPERING_MASK_B	0x9d2c5680
#define TEMPERING_MASK_C	0xefc60000

#define STATE_VECTOR_LENGTH 624
#define STATE_VECTOR_M      397 /* changes to STATE_VECTOR_LENGTH also require changes to this */

#define DATA_TYPE float

typedef struct tagMTRand {
  unsigned long mt[STATE_VECTOR_LENGTH];
  int index;
} MTRand;

MTRand seedRand(unsigned long seed);
unsigned long genRandLong(MTRand* rand);
DATA_TYPE box_muller(MTRand* rand);

static inline void m_seedRand(MTRand* rand, unsigned long seed) {
  /* set initial seeds to mt[STATE_VECTOR_LENGTH] using the generator
   * from Line 25 of Table 1 in: Donald Knuth, "The Art of Computer
   * Programming," Vol. 2 (2nd Ed.) pp.102.
   */
  rand->mt[0] = seed & 0xffffffff;
  for(rand->index=1; rand->index<STATE_VECTOR_LENGTH; rand->index++) {
    rand->mt[rand->index] = (6069 * rand->mt[rand->index-1]) & 0xffffffff;
  }
}

/**
* Creates a new random number generator from a given seed.
*/
MTRand seedRand(unsigned long seed) {
  MTRand rand;
  m_seedRand(&rand, seed);
  return rand;
}

/**
 * Generates a pseudo-randomly generated long.
 */
unsigned long genRandLong(MTRand* rand) {

  unsigned long y;
  static unsigned long mag[2] = {0x0, 0x9908b0df}; /* mag[x] = x * 0x9908b0df for x = 0,1 */
  if(rand->index >= STATE_VECTOR_LENGTH || rand->index < 0) {
    /* generate STATE_VECTOR_LENGTH words at a time */
    int kk;
    if(rand->index >= STATE_VECTOR_LENGTH+1 || rand->index < 0) {
      m_seedRand(rand, 4357);
    }
    for(kk=0; kk<STATE_VECTOR_LENGTH-STATE_VECTOR_M; kk++) {
      y = (rand->mt[kk] & UPPER_MASK) | (rand->mt[kk+1] & LOWER_MASK);
      rand->mt[kk] = rand->mt[kk+STATE_VECTOR_M] ^ (y >> 1) ^ mag[y & 0x1];
    }
    for(; kk<STATE_VECTOR_LENGTH-1; kk++) {
      y = (rand->mt[kk] & UPPER_MASK) | (rand->mt[kk+1] & LOWER_MASK);
      rand->mt[kk] = rand->mt[kk+(STATE_VECTOR_M-STATE_VECTOR_LENGTH)] ^ (y >> 1) ^ mag[y & 0x1];
    }
    y = (rand->mt[STATE_VECTOR_LENGTH-1] & UPPER_MASK) | (rand->mt[0] & LOWER_MASK);
    rand->mt[STATE_VECTOR_LENGTH-1] = rand->mt[STATE_VECTOR_M-1] ^ (y >> 1) ^ mag[y & 0x1];
    rand->index = 0;
  }
  y = rand->mt[rand->index++];
  y ^= (y >> 11);
  y ^= (y << 7) & TEMPERING_MASK_B;
  y ^= (y << 15) & TEMPERING_MASK_C;
  y ^= (y >> 18);
  return y;
}

DATA_TYPE box_muller(MTRand* rand, float *counter, int *max_convergence)	/* normal random variate generator */
{				        /* mean m, standard deviation s */
	DATA_TYPE x1, x2, w, _y1;
	static DATA_TYPE y2;
	static int use_last = 0;

    int counter2 = 0;

	if (use_last)		        /* use value from previous call */
	{
		_y1 = y2;
		use_last = 0;
	}
	else
	{
    // do {
		for(int i = 0; i < 100; i++) {
			x1 = 2.0 * ((DATA_TYPE)genRandLong(rand) / (unsigned long)0xffffffff) - 1.0;
			x2 = 2.0 * ((DATA_TYPE)genRandLong(rand) / (unsigned long)0xffffffff) - 1.0;
			w = x1 * x1 + x2 * x2;
      *counter += 1;
      counter2 += 1;
      
      if(w < 1) {
        break;
      }
		} //while(w >= 1.0);

        if(counter2 > *max_convergence) {
            *max_convergence = counter2;
        }

        // printf("%f\n", w);

		w = sqrt( (-2.0 * log( w ) ) / w );
		_y1 = x1 * w;
		y2 = x2 * w;
		use_last = 1;
	}

  DATA_TYPE result = (  _y1  );

	return result;
}

int main() {

    float counter = 0;
    int max_convergence = 0;

    int lower = 25;
    int upper = 75;

    for(int i; i < 1000; i++) {
        // Generate random number
        int S = (rand() % (upper - lower + 1)) + lower;

        // Seed RNG
        MTRand rand = seedRand(S);

        // Apply Box-Muller Transform
        for(int j; j < 1000; j++) {
            float test = box_muller(&rand, &counter, &max_convergence);
        }
    }

    // Calculate average rounds to convergence
    printf("Average # of rounds to convergence: %f\n", (counter / (100 * 1000)));
    printf("Maximum # of rounds to converge: %d\n", max_convergence);

    return 0;
}