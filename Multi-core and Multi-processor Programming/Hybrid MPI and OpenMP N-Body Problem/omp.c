#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define BODIES 5000
#define TIMESTEPS 100
#define GRAVCONST 0.0000001

// global vars
float mass[BODIES];
float vx[BODIES], vy[BODIES];
float x[BODIES], y[BODIES];
float dx, dy, d, F, ax, ay;

void testInit();
void testInit2();
void randomInit();
void outputBody(int);
int main(void) {
  omp_set_num_threads(16);
  int time, i, j;

  randomInit();

  for (time=0; time<TIMESTEPS; time++) {
    printf("Timestep %d\n",time);
    #pragma omp parallel for default(none) schedule(guided) \
    private(i, j, ax, ay, F, d, dx, dy) shared(x, y, vx, vy, mass)
    for (i=0; i<BODIES; i++) {
      // calc forces on body i due to bodies (j != i)
      for (j=0; j<BODIES; j++) {
        if (j != i) {
          dx = x[j] - x[i];
          dy = y[j] - y[i];
          d = sqrt(dx*dx + dy*dy); 
          if (d<0.01) {
            // printf("too close - resetting\n");
            d=1.0;
          }
          F = GRAVCONST * mass[i] * mass[j] / (d*d);
          ax = (F/mass[i]) * dx/d;
          ay = (F/mass[i]) * dy/d;
          vx[i] += ax;
          vy[i] += ay;
        }
      } // body j
    } // body i

    // having worked out all velocities we now apply and determine new position
    #pragma omp parallel for default(none) private(i) \
    shared(x, y, vx, vy) schedule(guided)
    for (i=0; i<BODIES; i++) {
      x[i] += vx[i];
      y[i] += vy[i];
      //DEBUG ONLY: outputBody(i);
    }

    printf("---\n");
  } // time
  printf("Final data\n");
  for (i=0; i<BODIES; i++) {
    outputBody(i);
  }
}


void randomInit() {
  int i;
//   #pragma omp parallel for default(none) private(i) \
//   shared(mass, x, y, vx, vy) schedule(guided)
  for (i=0; i<BODIES; i++) {
    mass[i] = 0.001 + (float)rand()/(float)RAND_MAX;            // 0.001 to 1.001

    x[i] = -250.0 + 500.0*(float)rand()/(float)RAND_MAX;   //  -10 to +10 per axis
    y[i] = -250.0 + 500.0*(float)rand()/(float)RAND_MAX;   //

    vx[i] = -0.2 + 0.4*(float)rand()/(float)RAND_MAX;   // -0.25 to +0.25 per axis
    vy[i] = -0.2 + 0.4*(float)rand()/(float)RAND_MAX;   
  }
  printf("Randomly initialised\n");
  return;
}

void outputBody(int i) {
  printf("Body %d: Position=(%f,%f) Velocity=(%f,%f)\n", i, x[i],y[i], vx[i],vy[i]);
  return;
}