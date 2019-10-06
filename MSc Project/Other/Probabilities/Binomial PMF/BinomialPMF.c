
// Program to calculate C(n ,k) 
#include <stdio.h>
#include <math.h>
  
// Function for c(n, r) modified from https://www.geeksforgeeks.org/space-and-time-efficient-binomial-coefficient/
double binomial_coeff(double n, double k)
{ 
    double res = 1; 
  
    // Since C(n, k) = C(n, n-k) 
    if ( k > n - k ) 
        k = n - k; 
  
    // Calculate value of [n * (n-1) *---* (n-k+1)] / [k * (k-1) *----* 1]
    for (int i = 0; i < k; ++i) 
    { 
        res *= (n - i);
        res /= (i + 1);
    } 
  
    return res; 
} 

// Function to calculate binomial probability mass function
// Formula on https://newonlinecourses.science.psu.edu/stat414/node/67/
double binomial_pmf(double n, double k, double p) {
    double nCk = binomial_coeff(n, k);
    double pmf = nCk * (double)pow(p, k) * (double)pow((1-p), (n-k));
    return pmf;
}
  
/* Driver program to test above function*/
int main() 
{ 
    double n = 20, k = 9, p=0.4;
    printf("nCk result is %f\n", binomial_coeff(n, k));
    printf("PMF Result is %f\n", binomial_pmf(n, k, p));
    return 0; 
} 