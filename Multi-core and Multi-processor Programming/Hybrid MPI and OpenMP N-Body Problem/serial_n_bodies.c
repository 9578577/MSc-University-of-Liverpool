#include <stdio.h>
#include <stdlib.h>

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
  int time, i, j;

  // testInit2();
  randomInit();

  for (time=0; time<TIMESTEPS; time++) {
    printf("Timestep %d\n",time);
    for (i=0; i<BODIES; i++) {
      // calc forces on body i due to bodies (j != i)
      for (j=0; j<BODIES; j++) {
	if (j != i) {
	  dx = x[j] - x[i];
	  dy = y[j] - y[i];
	  d = sqrt(dx*dx + dy*dy); 
	  if (d<0.01) {
	    printf("too close - resetting\n");
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


void testInit() {
    /* test: initial zero velocity ==> attraction only ie bodies should move closer together */
  int i;
  for (i=0; i<BODIES; i++) {
    mass[i] = 1.0;

    x[i] = (float) i;
    y[i] = (float) i;

    vx[i] = 0.0;
    vy[i] = 0.0;
  }
}

void testInit2() {
  /* test data */
  mass[0] = 1.0;
  x[0]=0.0;
  y[0]=0.0;
  vx[0]=0.01;
  vy[0]=0.0;
  mass[1] = 0.1;
  x[1]=1.;
  y[1]=1.;
  vx[1]=0.;
  vy[1]=0.;
  mass[2] = .001;
  x[2]=0.;;
  y[2]=1.;
  vx[2]=.01;
  vy[2]=-.01;
}

void outputBody(int i) {
  printf("Body %d: Position=(%f,%f) Velocity=(%f,%f)\n", i, x[i],y[i], vx[i],vy[i]);
  return;
}