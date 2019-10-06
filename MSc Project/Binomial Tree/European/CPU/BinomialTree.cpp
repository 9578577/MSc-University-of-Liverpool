/*
 * Matthew Carter - University of Liverpool
 * General Addititve Binomial Valuation of European Options
 */

#include "BinomialTree.h"

DATA_TYPE binomial_tree(DATA_TYPE S, DATA_TYPE K, DATA_TYPE T, DATA_TYPE D, DATA_TYPE r, DATA_TYPE v, int type, int height) {
    // Compute starting constants
    DATA_TYPE dt = T / (DATA_TYPE)height;
    DATA_TYPE sqrt_dt = sqrt(dt);
    DATA_TYPE u = exp(((r - D) * dt) + (v * sqrt_dt));
    DATA_TYPE d = exp(((r - D) * dt) - (v * sqrt_dt));
    DATA_TYPE pu = (exp((r - D) * dt) - d) / (u - d);
    DATA_TYPE pd = 1 - pu;
    DATA_TYPE disc = exp(-r * dt);
    DATA_TYPE dpu = disc * pu;
    DATA_TYPE dpd = disc * pd;

    DATA_TYPE C[MAX_TREE_HEIGHT];
    DATA_TYPE St[MAX_TREE_HEIGHT];

    // Initialise asset prices at maturity
    for(int i = 0; i < height; i++) {
        St[i] = S * pow(u, (height-i)) * pow(d, i);
    }

    // Initialise option values at maturity
    if(type == 0) {
        for(int i = 0; i < height; i++) {
            // Call value
            C[i] = max(St[i] - K, 0);
        }
    } else {
        for(int i = 0; i < height; i++) {
            // Put value
            C[i] = max(K - St[i], 0);
        }
    }

    // Step back through tree
    for(int i = height-1; i >= 0; i--) {
        for(int j = 0; j <= i; j++) {
            // Binomial value
            C[j] = (dpu * C[j]) + (dpd * C[j+1]);
        }
    }

    return C[0];
}

int main() {
    struct timeval stop, start;

    // Arrays to hold option data
    DATA_TYPE output[MAX_ENTRIES];
    DATA_TYPE S[MAX_ENTRIES];
    DATA_TYPE K[MAX_ENTRIES];
    DATA_TYPE T[MAX_ENTRIES];
    DATA_TYPE D[MAX_ENTRIES];
    DATA_TYPE r[MAX_ENTRIES];
    DATA_TYPE v[MAX_ENTRIES];
    int type[MAX_ENTRIES];
    int height[MAX_ENTRIES];

    FILE* file = fopen("./option_data.txt", "r");
    char linebuf[512];
    int i = 0;

    // Check that the data file was read
    if (file == NULL) {
        std::cout << "[ERROR] Unable to open data file" << std::endl;
        exit(0);
    }

    // Read the data
    while(fgets(linebuf, sizeof(linebuf), file) != NULL) {
        if(i >= 25) {
            std::cout << "[WARNING] Reached maximum number of options" << std::endl;
            break;
        }

        // Skip hashtags and new lines
        if(linebuf[0] == '#' || linebuf[0] == '\n') {
            continue;
        }

        // Allocate data to arrays
        sscanf(linebuf, "%f,%f,%f,%f,%f,%f,%d,%d", &S[i], &K[i], &T[i], &D[i], &r[i], &v[i], &type[i], &height[i]);

        i++;
    }

    // Ensure that height doesn't exceed max tree height
    for(int j = 0; j < i; j++) {
        if(height[j] >= MAX_TREE_HEIGHT) {
            height[j] = MAX_TREE_HEIGHT;
        }
    }

    std::cout << "Calculating option prices..." << std::endl;

    // Calculate prices of options
    gettimeofday(&start, NULL);
    for(int j = 0; j < i; j++) {
        output[j] = binomial_tree(S[j], K[j], T[j], D[j], r[j], v[j], type[j], height[j]);
    }
    gettimeofday(&stop, NULL);

    // Output results
    std::cout << "================================\n" << std::endl;
    std::cout << "=========== RESULTS ============\n" << std::endl;
    std::cout << "================================\n" << std::endl;
    for(int j = 0; j < i; j++) {
        if(type[j] == 0) {
            std::cout << std::setprecision(8) << "[" << j << "] Call price: $" << output[j] << std::endl;
        } else {
            std::cout << std::setprecision(8) << "[" << j << "] Put price: $" << output[j] << std::endl;
        }
    }
    std::cout << "================================\n" << std::endl;
    std::cout << std::setprecision(8) << "Execution time: " << (double) (stop.tv_usec - start.tv_usec) / 1000000 + (double) (stop.tv_sec - start.tv_sec) << " seconds" << std::endl;
    std::cout << "================================\n" << std::endl;

    return 0;
}