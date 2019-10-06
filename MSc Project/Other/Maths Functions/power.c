#include <stdio.h>
#include <math.h>

int main() {

    int N = 5;
    float x = 2;
    float result = 0;

    printf("Power function:\n");
    for(int i = 0; i < N; i++) {
        printf("%f\n", pow(x, i));
    }

    printf("\n");

    printf("Power for loop:\n");
    
    for(int i = 0; i < N; i++) {
        if (i == 0) {
            result = 1;
        } else {
            result *= x;
        }
        printf("%f\n", result);
    }

    return 0;
}