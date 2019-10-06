#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

// // Number of steps to take between the lower and upper bound
// #define N 10000000

__global__ void initCalcKernel(double *x_dev, double *y_dev, double x1, double stepSize, int N)
{
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    // Ensure that i does not exceed N
    if(i < N) {
        // Calculate each value of x used to calculate f(x)
        x_dev[i] = x1 + (i * stepSize);
        __syncthreads();
        y_dev[i] = exp(-((x_dev[i]-2) * (x_dev[i]-2))) + exp(-((x_dev[i]-6) * (x_dev[i]-6)) / 10) + (1 / ((x_dev[i] * x_dev[i]) + 1));
    }
}

int main(int argc, char *argv[]) 
{
    omp_set_num_threads(16);
    int i;
    char *ptr;
    int N = strtol(argv[1], &ptr, 10);

    // Set up timers
    cudaEvent_t initCalcStart, initCalcStop, memcpyStart, memcpyStop;
    cudaEventCreate(&initCalcStart); cudaEventCreate(&initCalcStop);
    cudaEventCreate(&memcpyStart); cudaEventCreate(&memcpyStop);
    double maximisationStart, maximisationStop;
    double totalStart, totalStop;
    
    totalStart = omp_get_wtime();

    // Set up the problem
    double x1 = -100.0, x2 = 100.0; // Upper and lower bounds of x
    double stepSize = (x2 - x1) / N; // Size of the steps between the upper and lower bound

    // Calculate the number of blocks and threads per block to use
    int threadsPerBlock, maxThreadsPerBlock=1024;
    threadsPerBlock = N > maxThreadsPerBlock ? maxThreadsPerBlock : N;
    int blocks = ceil(N / threadsPerBlock);

    // Define variable to hold values of x and y on host and GPU
    double *x, *x_dev, *y, *y_dev;
    x = (double *) malloc(N*sizeof(*x));
    cudaMalloc(&x_dev, N*sizeof(double));
    y = (double *) malloc(N*sizeof(*y));
    cudaMalloc(&y_dev, N*sizeof(double));

    // Call initialisation kernel
    cudaEventRecord(initCalcStart,0);
    initCalcKernel<<<blocks, threadsPerBlock>>> (x_dev, y_dev, x1, stepSize, N);
    cudaEventRecord(initCalcStop,0);

    // Check for errors
    cudaError e = cudaGetLastError();
    if(e != cudaSuccess) {
      printf("CUDA ERROR: %s \n", cudaGetErrorString(e));
    }

    // Bring data back to host
    cudaEventRecord(memcpyStart,0);
    cudaMemcpy(x, x_dev, N*sizeof(double), cudaMemcpyDeviceToHost);
    cudaMemcpy(y, y_dev, N*sizeof(double), cudaMemcpyDeviceToHost);
    cudaEventRecord(memcpyStop,0);

    // Check for errors
    e = cudaGetLastError();
    if(e != cudaSuccess) {
      printf("CUDA ERROR: %s \n", cudaGetErrorString(e));
    }

    // Syncrhonise host and GPU
    cudaDeviceSynchronize();

    // Variables to store the maximum value of f(x)
    // and the value of x that maximises f(x)
    double max = y[0]; 
    double my_max = y[0];
    double max_x = 0;
    double my_max_x = 0; 

    // Calculate the maximum of f(x)
    maximisationStart = omp_get_wtime();
    #pragma omp parallel default(none) shared(x, y, max, max_x, N) private(i, my_max, my_max_x)
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

    // CUDA timing
    float initCalcTime, memcpyTime;
    cudaEventElapsedTime(&initCalcTime, initCalcStart, initCalcStop);
    cudaEventElapsedTime(&memcpyTime, memcpyStart, memcpyStop);

    // Print output to command line - we divide CUDA's timings by 1000 to convert from milliseconds to seconds
    printf("----------------------CUDA IMPLEMENTATION OUTPUT----------------------\n");
    printf("Matthew Carter | Student ID 201371920 | COMP528 Assignment 3 Output\n");
    printf("--------------------------------OUTPUT--------------------------------\n");
    printf("Calcuating maximum with %d steps and a step size of %.8f\n", N, stepSize);
    printf("Using %d blocks and %d threads per block\n", blocks, threadsPerBlock);
    printf("--------------------------------RESULT--------------------------------\n");
    printf("Maximum value of f(x) = %.15f when x = %.15f\n", max, max_x);
    printf("--------------------------------TIMING--------------------------------\n");
    printf("Time taken to initialise and calculate f(x) %f seconds\n", (initCalcTime / 1000));
    printf("Time taken to copy data to host %f seconds\n", (memcpyTime / 1000));
    printf("Time taken to maximse f(x) %f seconds\n", (maximisationStop - maximisationStart));
    printf("Total time taken %f seconds\n", (totalStop - totalStart));
    printf("----------------------------------------------------------------------\n");


    // Free allocated memory
    free(x);
    free(y);
    cudaFree(x_dev);
    cudaFree(y_dev);

    return 0;

}