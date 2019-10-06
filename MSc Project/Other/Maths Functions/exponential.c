#include <stdio.h>
#include <math.h>
#include <time.h>

int main() {
    float x = 5;
    int n = 15;
    float result = 1;

    printf("Exponential function:\n");
    printf("%f\n", exp(x));

    printf("\n");

    // https://www.geeksforgeeks.org/program-to-efficiently-calculate-ex/
    printf("For loop exponential:\n");
    for(int i = n - 1; i > 0; --i) {
        result = 1 + x * result / (float)i;
    }
    printf("%f\n", result);
}