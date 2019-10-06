#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define BODIES 5000
#define TIMESTEPS 100
#define GRAVCONST 0.0000001

// global vars
float mass[BODIES];
float vx[BODIES], vy[BODIES];
float x[BODIES], y[BODIES];
float dx, dy, d, F, ax, ay;
int world_size, world_rank;

void randomInit();
void outputBody(int);
int main(void) {
  MPI_Init(NULL, NULL);
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

  if((BODIES % world_size) > 0) {
    printf("[ERROR] The number of bodies used must be divisible by the number of processes");
    MPI_Abort(MPI_COMM_WORLD, -1);
  }

  int time, i, j;
  int bodies_per_process, offset;
  bodies_per_process = BODIES / world_size;
  offset = bodies_per_process * world_rank;

  // Assign loc_x and loc_y to hold the positions of each body at each timestep
  float loc_x[bodies_per_process], loc_y[bodies_per_process];

  printf("[%d] Bodies per process: %d | Offset: %d\n", world_rank, bodies_per_process, offset);

  // Initialise the problem on process zero
  if (world_rank == 0) {
    randomInit();
  }

  // Broadcast the data to all processes
  MPI_Bcast(&mass, BODIES, MPI_FLOAT, 0, MPI_COMM_WORLD);
  MPI_Bcast(&vx, BODIES, MPI_FLOAT, 0, MPI_COMM_WORLD);
  MPI_Bcast(&vy, BODIES, MPI_FLOAT, 0, MPI_COMM_WORLD);
  MPI_Bcast(&x, BODIES, MPI_FLOAT, 0, MPI_COMM_WORLD);
  MPI_Bcast(&y, BODIES, MPI_FLOAT, 0, MPI_COMM_WORLD);

  if(world_rank == 0) printf("[%d] Data broadcast to all ranks\n", world_rank);

  for (time=0; time<TIMESTEPS; time++) {
    printf("[%d] Timestep %d\n", world_rank, time);
    #pragma omp parallel default(none) private(i, j, ax, ay, F, d, dx, dy) \
    shared(x, y, vx, vy, mass, loc_x, loc_y, offset, bodies_per_process)
    {
      #pragma omp for schedule(guided)
      for (i=0; i<bodies_per_process; i++) {
        // calc forces on body i due to bodies (j != i)
        for (j=0; j<BODIES; j++) {
          if (j != i) {
            dx = x[j + offset] - x[i + offset];
            dy = y[j + offset] - y[i + offset];
            d = sqrt(dx*dx + dy*dy); 
            if (d<0.01) {
              // printf("too close - resetting\n");
              d=1.0;
            }
            F = GRAVCONST * mass[i + offset] * mass[j + offset] / (d*d);
            ax = (F/mass[i + offset]) * dx/d;
            ay = (F/mass[i + offset]) * dy/d;
            vx[i + offset] += ax;
            vy[i + offset] += ay;
          }
        } // body j
      } // body i

      #pragma omp for schedule(guided)
      for (i=0; i<bodies_per_process; i++) {
        loc_x[i] = x[i + offset] + vx[i + offset];
        loc_y[i] = y[i + offset] + vy[i + offset];
        // outputBody(i);
      }
    }
    
    // Bring all the results back into x and y
    MPI_Allgather(&loc_x, bodies_per_process, MPI_FLOAT, &x,  bodies_per_process, MPI_FLOAT, MPI_COMM_WORLD);
    MPI_Allgather(&loc_y, bodies_per_process, MPI_FLOAT, &y,  bodies_per_process, MPI_FLOAT, MPI_COMM_WORLD);

    printf("---\n");
  } // time

  // Do this on rank zero

  if(world_rank == 0) {
    printf("Final data\n");
    for (i=0; i<BODIES; i++) {
      outputBody(i);
    }
  }

  MPI_Finalize();
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
  printf("[%d] Randomly initialised\n", world_rank);
  return;
}

void outputBody(int i) {
  printf("Body %d: Position=(%f,%f) Velocity=(%f,%f)\n", i, x[i],y[i], vx[i],vy[i]);
  return;
}