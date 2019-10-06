#include <stdio.h>
#include <stdlib.h> // For memory allocation
#include <math.h> // For sin function
#include <mpi.h>

// Global Variables
int world_size, world_rank;
double initialisation_start, initialisation_stop, initialisation_time, calculation_start, calculation_stop, calculation_time;

int main(int argc, char *argv[])
{
  // Initialise MPI
  MPI_Init(NULL, NULL);
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

  // Start initialisation timer
  initialisation_start = MPI_Wtime();

  // array_size determines how many elements the arrays a and b should be populated with
  int array_size;
  double *a, *b;

  // Initialise the problem on process zero
  if(world_rank == 0) {
    // Pull the array size from the argument specified when running, if no argument is specified set array_size equal to 2,000,000
    char *ptr;
    array_size = argv[1] != 0 ? strtol(argv[1], &ptr, 10) : 2000000;

    // allocate memory for a and b based on the size of a double and the array_size
    a = (double *) malloc(sizeof(double) * array_size);
    b = (double *) malloc(sizeof(double) * array_size);

    // Populate arrays
    for(int i = 0; i < array_size; i++) {
    a[i] = sin(i);
    b[i] = sin(i + 5);
    }
  }

  // Broadcast the array_size to all processes
  MPI_Bcast(&array_size, 1, MPI_INT, 0, MPI_COMM_WORLD);

  // Calculate the number of elements each process should handle and any remainder
  // If there is a remainder, let the last process handle this extra load
  int remainder = array_size % world_size;
  int elements_per_process = world_rank == world_size - 1 ? (array_size / world_size) + remainder : (array_size / world_size);

  // Create an array of sendcount and the location of each send for each process
  int* sendcount = malloc(sizeof(int) * world_size);
  int* displs = malloc(sizeof(int) * world_size);
  for (int i = 0; i < world_size; i++) {
    if (world_rank == 0) {
      displs[i] = elements_per_process * i;
      sendcount[i] = i == world_size - 1 ? elements_per_process + remainder : elements_per_process;
    }
  }

  // Create a local array for a and b based on how many elements each process will handle
  double* loc_a = malloc(sizeof(double) * elements_per_process);
  double* loc_b = malloc(sizeof(double) * elements_per_process);

  // Distribute the elements of a and b to each process
  MPI_Scatterv(&a[0], sendcount, displs, MPI_DOUBLE, &loc_a[0], elements_per_process, MPI_DOUBLE, 0, MPI_COMM_WORLD);
  MPI_Scatterv(&b[0], sendcount, displs, MPI_DOUBLE, &loc_b[0], elements_per_process, MPI_DOUBLE, 0, MPI_COMM_WORLD);

  // Synchronise processes for timing
  MPI_Barrier(MPI_COMM_WORLD);

  // END INITIALISATION TIMER AND CALCULATE TIME TAKEN
  initialisation_stop = MPI_Wtime();
  initialisation_time = initialisation_stop - initialisation_start;

  // START CALCULATION TIMER
  calculation_start = MPI_Wtime();

  // Create a set of local variables to hold the mean of a and b
  double loc_mean_a, loc_mean_b = 0;

  // Calculate the sum of a and b
  for(int i = 0; i < elements_per_process; i++) {
    loc_mean_a += loc_a[i];
    loc_mean_b += loc_b[i];
  }

  // Calculate the mean
  loc_mean_a = loc_mean_a / array_size;
  loc_mean_b = loc_mean_b / array_size;

  // Define global variables for the mean of a and b and reduce
  double glob_mean_a, glob_mean_b = 0;

  // Use MPI_Allreduce to sum the means and then broadcast the result to each process
  MPI_Allreduce(&loc_mean_a, &glob_mean_a, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
  MPI_Allreduce(&loc_mean_b, &glob_mean_b, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

  // Variables for the variance and standard deviation of a and b
  double loc_dist_a, loc_dist_b = 0;
  double loc_var_a, loc_var_b = 0;
  double loc_std_a, loc_std_b = 0;
  double loc_covar_a_b = 0;

  // Calculate the distance between a and b and their respective means
  // Calculate the variance of a and b
  // Calculate covariance of a and b
  for (int i = 0; i < elements_per_process; i++) {
    loc_dist_a = loc_a[i] - glob_mean_a;
    loc_dist_b = loc_b[i] - glob_mean_b;
    loc_var_a += loc_dist_a * loc_dist_a;
    loc_var_b += loc_dist_b * loc_dist_b;
    loc_covar_a_b += loc_dist_a * loc_dist_b;
  }

  // Calculate standard deviation and covariance
  loc_var_a = loc_var_a / array_size;
  loc_var_b = loc_var_b / array_size;
  loc_covar_a_b = loc_covar_a_b / array_size;

  // Define global variables for standard deviation and covariance
  double glob_var_a, glob_var_b = 0;
  double glob_covar_a_b = 0;

  // Reduce and sum on core zero
  MPI_Reduce(&loc_var_a, &glob_var_a, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
  MPI_Reduce(&loc_var_b, &glob_var_b, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
  MPI_Reduce(&loc_covar_a_b, &glob_covar_a_b, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);


  // Calculate the standard deviation, pearson correlation and create an output on process zero
  if (world_rank == 0) {
    // Calculate global std of a and b
    double glob_std_a = sqrt(glob_var_a);
    double glob_std_b = sqrt(glob_var_b);

    // Calculate the pearson correlation
    double pearson_correlation = glob_covar_a_b / (glob_std_a * glob_std_b);

    // END CALCULATION TIMER AND CALCULATE TIME TAKEN
    calculation_stop = MPI_Wtime();
    calculation_time = calculation_stop - calculation_start;

    // Free up allocated memory
    free(loc_a);
    free(loc_b);
    free(sendcount);
    free(displs);

    // Produce output from process zero
    printf("------------------------- OUTPUT -------------------------\n");
    printf("Processes used: %d; Array size: %d; Remainder: %d\n", world_size, array_size, remainder);
    printf("----------------------------------------------------------\n");
    printf("Mean of a: %.4f and b: %.4f\n", glob_mean_a, glob_mean_b);
    printf("Variance of a: %.4f and b: %.4f\n", glob_var_a, glob_var_b);
    printf("Standard deviation of a: %.4f and b: %.4f\n", glob_std_a, glob_std_b);
    printf("Covariance of a and b: %.4f\n", glob_covar_a_b);
    printf("Pearson correlation of a and b: %.4f\n", pearson_correlation);
    printf("----------------------------------------------------------\n");
    printf("Time taken to intialise the problem: %f\n", initialisation_time);
    printf("Time taken to calculate the pearson correlation: %f\n", calculation_time);
    printf("Total time taken: %f\n", initialisation_time + calculation_time);
    printf("----------------------------------------------------------\n");
  }

  // Finalise MPI
  MPI_Finalize();
  return 0;
}
