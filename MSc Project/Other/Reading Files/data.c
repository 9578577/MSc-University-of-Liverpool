#include <stdio.h>
#include <stdlib.h>

#define MAX_ENTRIES 25
#define DATA_TYPE float

int main() {

    // Arrays to hold option data
    DATA_TYPE S[MAX_ENTRIES];
    DATA_TYPE K[MAX_ENTRIES];
    DATA_TYPE T[MAX_ENTRIES];
    DATA_TYPE D[MAX_ENTRIES];
    DATA_TYPE r[MAX_ENTRIES];
    DATA_TYPE v[MAX_ENTRIES];
    int type[MAX_ENTRIES];
    int steps[MAX_ENTRIES];

    FILE* file = fopen("option_data.txt", "r");
    char linebuf[512];
    int i = 0;

    // Check that the data file was read
    if (file == NULL) {
        printf("[ERROR] Unable to open data file\n");
        exit(0);
    }

    // Read the data
    while(fgets(linebuf, sizeof(linebuf), file) != NULL) {
        if(i >= 25) {
            printf("[ERROR] Reached maximum number of options\n");
            break;
        }

        // Skip hashtags and new lines
        if(linebuf[0] == '#' || linebuf[0] == '\n') {
            continue;
        }

        // Allocate data to arrays
        sscanf(linebuf, "%f,%f,%f,%f,%f,%f,%d,%d", &S[i], &K[i], &T[i], &D[i], &r[i], &v[i], &type[i], &steps[i]);

        i++;
    }

    printf("Data read\n");

    for(int j = 0; j < i; j++) {
        printf("[%d] %f %f %f %f %f %f %d %d\n", j, S[j], K[j], T[j], D[j], r[j], v[j], type[j], steps[j]);
    }

    fclose(file);

    return 0;
}