#include <stdio.h>
#include <stdlib.h> // For memory allocation
#include <math.h> // For sin and sqrt function
#include <omp.h>

double init_start, init_stop, init_time, calc_start, calc_stop, calc_time;

int main(int argc, char *argv[])
{
  int array_size, i;
  char *ptr;

  if(argc != 3) {
    printf("Not all arguments were entered, setting number of threads equal to 2 and array size equal to 2,000,000\n");
    printf("To specify no. of threads and array size use: ./parallel_pearson_correlation.exe t n where t is the number of threads and n is array size\n");
    omp_set_num_threads(2);
    array_size = 2000000;
  } else {
    omp_set_num_threads(strtol(argv[1], &ptr, 10));
    array_size = strtol(argv[2], &ptr, 10);
  }  

  // Start initialisation timer
  init_start = omp_get_wtime();

  // Define variables
  double* a = malloc(sizeof(double) * array_size);
  double* b = malloc(sizeof(double) * array_size);
  double mean_a, mean_b = 0;

  // Populate the arrays in parallel and calculate the sum of a and b
  #pragma omp parallel for default(none) shared(a, b, array_size) \
    private(i) reduction(+:mean_a,mean_b) schedule(guided)
  for (i = 0; i < array_size; i++) {
    // Populate arrays a and b
    a[i] = sin(i);
    b[i] = sin(i + 5);
    // Calculate the sum of a and b ready for calculating mean
    mean_a += a[i];
    mean_b += b[i];
  }

  // End time
  init_stop = omp_get_wtime();

  // Start time
  calc_start = omp_get_wtime();

  // Calculate the mean of a and b
  // This can be done in parallel by using tasks on two threads
  #pragma omp parallel sections num_threads(2)
  {
    #pragma omp section
      mean_a = mean_a / array_size;
    #pragma omp section
      mean_b = mean_b / array_size;
  }

  // Calculate the numerator of the variance and covariane equations
  // We will divide these by array_size before calculating the pearson correlation
  double dist_a, dist_b, var_a, var_b, covar_ab = 0;
  #pragma omp parallel for default(none) shared(a, b, array_size, mean_a, mean_b) \
    private(i, dist_a, dist_b) reduction(+:var_a,var_b,covar_ab) schedule(guided)
  for(i = 0; i < array_size; i++) {
    // Calculate distance
    dist_a = a[i] - mean_a;
    dist_b = b[i] - mean_b;
    // Calculate variance
    var_a += dist_a * dist_a;
    var_b += dist_b * dist_b;
    // Calculate covariance
    covar_ab += dist_a * dist_b;
  }

  // Calculate the standard deviation of a and b
  // This can also be done in parallel by using tasks
  double std_a, std_b = 0;
  #pragma omp parallel sections num_threads(2)
  {
    #pragma omp section
      std_a = sqrt(var_a / array_size);
    #pragma omp section
      std_b = sqrt(var_b / array_size);
  }

  // Calculate covariance and pearson correlation
  covar_ab = covar_ab / array_size;
  double pearson_correlation = covar_ab / (std_a * std_b);

  // End time
  calc_stop = omp_get_wtime();

  // Calculate time taken
  init_time = init_stop - init_start;
  calc_time = calc_stop - calc_start;

  // Print final output
  printf("------------------------- OUTPUT -------------------------\n");
  printf("Array size: %d\n", array_size);
  printf("----------------------------------------------------------\n");
  printf("Mean of a: %.4f and b: %.4f\n", mean_a, mean_b);
  printf("Variance of a: %.4f and b: %.4f\n", (var_a / array_size), (var_b / array_size));
  printf("Standard deviation of a: %.4f and b: %.4f\n", std_a, std_b);
  printf("Covariance of a and b: %.4f\n", covar_ab);
  printf("Pearson correlation of a and b: %.4f\n", pearson_correlation);
  printf("----------------------------------------------------------\n");
  printf("Time taken to intialise the problem: %f\n", init_time);
  printf("Time taken to calculate the pearson correlation: %f\n", calc_time);
  printf("Total time taken: %f\n", init_time + calc_time);
  printf("----------------------------------------------------------\n");

  // Free up allocated memory
  free(a);
  free(b);
}