#include <stdio.h>
#include <stdlib.h> // For memory allocation
#include <math.h> // For sin and sqrt function
#include <time.h> // Timing

// Global Variables to hold timing
double initialisation_start, initialisation_stop, initialisation_time, calculation_start, calculation_stop, calculation_time;

int main(int argc, char *argv[])
{
  int i; // i for for loops

  // Start initiaisation timer - adapted from https://www.tutorialspoint.com/c_standard_library/c_function_clock.htm
  clock_t initialisation_start, initialisation_stop;
  initialisation_start = clock();

  // Pull the array size from the argument specified when running, if no argument is specified set array_size equal to 2,000,000
  char *ptr;
  int array_size = argv[1] != 0 ? strtol(argv[1], &ptr, 10) : 2000000;

  // Create a pointer array based on the size of array_size
  double* a = malloc(sizeof(double) * array_size);
  double* b = malloc(sizeof(double) * array_size);

  // Variables to hold the mean of a and b
  double mean_a, mean_b = 0;

  for(i = 0; i < array_size; i++) {
    // Populate the a and b with numbers
    a[i] = sin(i);
    b[i] = sin(i + 5);

    // Calculate the sum of a and b ready to calculate the mean
    mean_a += a[i];
    mean_b += b[i];
  }

  // Stop initialisation timer & calculate time taken
  initialisation_stop = clock() - initialisation_start;
  initialisation_time = ((double)initialisation_stop)/CLOCKS_PER_SEC;
  // Start calculation timer
  clock_t calculation_start, calculation_stop;
  calculation_start = clock();

  // Calculate mean of a and b
  mean_a = mean_a / array_size;
  mean_b = mean_b / array_size;

  // Variables to store the variance, standard devation and covariance of a and b
  double distance_a, distance_b = 0;
  double var_a, var_b = 0;
  double std_a,  std_b = 0;
  double covar_a_b = 0;

  // Calculate variance, standard deviation and covariance of a and b
  for(i = 0; i < array_size; i++) {
      // Calculate the distance between the variable and respective mean
      distance_a = a[i] - mean_a;
      distance_b = b[i] - mean_b;

      // Calculate the squared distances of a and b
      var_a += distance_a * distance_a;
      var_b += distance_b * distance_b;

      // Calculate the product of a and b
      covar_a_b += distance_a * distance_b;
  }

  // Calculate standard deviation and covariance
  std_a = sqrt(var_a / array_size);
  std_b = sqrt(var_b / array_size);
  covar_a_b = covar_a_b / array_size;

  // Calculate pearson correlation
  double pearson_correlation = covar_a_b / (std_a * std_b);

  // Stop calculation timer and calculate time taken
  calculation_stop = clock() - calculation_start;
  calculation_time = ((double)calculation_stop)/CLOCKS_PER_SEC;

  // Free allocated memory
  free(a);
  free(b);

  // PRINT OUTPUT
  printf("------------------------- OUTPUT -------------------------\n");
  printf("Array size: %d\n", array_size);
  printf("----------------------------------------------------------\n");
  printf("Mean of a: %.4f and b: %.4f\n", mean_a, mean_b);
  printf("Variance of a: %.4f and b: %.4f\n", (var_a / array_size), (var_b / array_size));
  printf("Standard deviation of a: %.4f and b: %.4f\n", std_a, std_b);
  printf("Covariance of a and b: %.4f\n", covar_a_b);
  printf("Pearson correlation of a and b: %.4f\n", pearson_correlation);
  printf("----------------------------------------------------------\n");
  printf("Time taken to intialise the problem: %f\n", initialisation_time);
  printf("Time taken to calculate the pearson correlation: %f\n", calculation_time);
  printf("Total time taken: %f\n", initialisation_time + calculation_time);
  printf("----------------------------------------------------------\n");

  return 0;
}
