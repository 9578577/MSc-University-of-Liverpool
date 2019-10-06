#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

int main(int argc, char *argv[]) 
{
    // Variables to hold timings
    double initialisationStart, initialisationStop;
    double functionStart, functionStop;
    double maximisationStart, maximisationStop;
    double totalStart, totalStop;

    // Set omp threads and i
    omp_set_num_threads(16);
    int i;

    totalStart = omp_get_wtime();

    // Set up the problem
    double x1 = -100.0, x2 = 100.0; // Upper and lower bounds of x
    char *ptr;
    int N = strtol(argv[1], &ptr, 10); // Number of steps to take between the lower and upper bound
    double stepSize = (x2 - x1) / N; // Size of the steps between the upper and lower bound

    // Define variable to hold values of x
    double* x = malloc(sizeof(double) * N);

    // Calculate values of x and store them
    initialisationStart = omp_get_wtime();
    #pragma omp parallel for default(none) shared(x, N, stepSize, x1) \
    private(i) schedule(guided)
    for(i = 0; i < N; i++) {
        x[i] = x1 + (i * stepSize);
    }
    initialisationStop = omp_get_wtime();

    // Define variable to hold values of f(x[i])
    double* y = malloc(sizeof(double) * N);

    // Calculate values of f(x[i])
    functionStart = omp_get_wtime();
    #pragma omp parallel for default(none) shared(y, x, N) private(i) schedule(guided)
    for(i = 0; i < N; i++) {
        // Define function
        y[i] = exp(-((x[i]-2) * (x[i]-2))) + exp(-((x[i]-6) * (x[i]-6)) / 10) + (1 / ((x[i] * x[i]) + 1));
    }
    functionStop = omp_get_wtime();

    // Variables to store the maximum value of f(x)
    // and the value of x that maximises f(x)
    double max = y[0]; 
    double my_max = y[0];
    double max_x = 0;
    double my_max_x = 0; 

    // Calculate the maximum of f(x)
    maximisationStart = omp_get_wtime();
    #pragma omp parallel default(none) shared(x, y, N, max, max_x) private(i, my_max, my_max_x)
    {
        #pragma omp for
        for(i = 0; i < N; i++) {
            if(y[i] > my_max) {
                my_max = y[i];
                my_max_x = x[i];
            }
        }

        #pragma omp critical
        {
            if(my_max > max) {
                max = my_max;
                max_x = my_max_x;
            }
        }
    }
    maximisationStop = omp_get_wtime();
    totalStop = omp_get_wtime();

    // Print output to command line
    printf("---------------------OPENMP IMPLEMENTATION OUTPUT---------------------\n");
    printf("Matthew Carter | Student ID 201371920 | COMP528 Assignment 3 Output\n");
    printf("--------------------------------OUTPUT--------------------------------\n");
    printf("Calcuating maximum with %d steps and a step size of %.8f\n", N, stepSize);
    printf("--------------------------------RESULT--------------------------------\n");
    printf("Maximum value of f(x) = %.15f when x = %.15f\n", max, max_x);
    printf("--------------------------------TIMING--------------------------------\n");
    printf("Time taken to initialise the problem %f seconds\n", (initialisationStop - initialisationStart));
    printf("Time taken to calculate f(x) %f seconds\n", (functionStop - functionStart));
    printf("Time taken to maximse the function %f seconds\n", (maximisationStop - maximisationStart));
    printf("Total time taken %f seconds\n", (totalStop - totalStart));
    printf("----------------------------------------------------------------------\n");

    // Free stored memory
    free(x);
    free(y);
    return 0;

}