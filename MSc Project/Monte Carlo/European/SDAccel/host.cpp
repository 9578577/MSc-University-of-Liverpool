#include "xcl2.hpp"
#include <stdlib.h>
#include <vector>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <cmath>
#include <sys/time.h>

#define DATA_TYPE float

#ifndef max
    #define max(x, y) (((x) > (y)) ? (x) : (y))
#endif

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cout << "Usage: " << argv[0] << " <XCLBIN File>" << std::endl;
        return EXIT_FAILURE;
    }

    std::string binaryFile = argv[1];
    cl_int err;
    unsigned fileBufSize;
    struct timeval stop, start;

    // Start timer
    gettimeofday(&start, NULL);

    // Set starting variables
    DATA_TYPE S = 50;
    DATA_TYPE K = 50;
    DATA_TYPE T = 1;
    DATA_TYPE D = 0;
    DATA_TYPE r = 0.05;
    DATA_TYPE v = 0.2;
    int type_r = 1;
    int M = 1000000;
    int N = 100;

    // Allocate output memory
    std::vector<DATA_TYPE, aligned_allocator<DATA_TYPE>> output(M * sizeof(DATA_TYPE));

    // Find Xilinx platforms and return a list of devices
    auto devices = xcl::get_xil_devices();
    auto device = devices[0];

    OCL_CHECK(err, cl::Context context(device, NULL, NULL, NULL, &err));
    OCL_CHECK(err, cl::CommandQueue q(context, device, CL_QUEUE_PROFILING_ENABLE, &err));

    // Read in binary file
    auto fileBuf = xcl::read_binary_file(binaryFile, fileBufSize);
    cl::Program::Binaries bins{{fileBuf, fileBufSize}};

    devices.resize(1);
    OCL_CHECK(err, cl::Program program(context, devices, bins, NULL, &err));
    OCL_CHECK(err, cl::Kernel kernel(program, "eu_monte_carlo", &err));

    // Allocate buffers in global memory
    OCL_CHECK(err,
              cl::Buffer buffer_output(context,
                                    CL_MEM_USE_HOST_PTR | CL_MEM_READ_ONLY,
                                    M * sizeof(DATA_TYPE),
                                    output.data(),
                                    &err));

    int narg = 0;
    OCL_CHECK(err, err = kernel.setArg(narg++, buffer_output));
    OCL_CHECK(err, err = kernel.setArg(narg++, S));
    OCL_CHECK(err, err = kernel.setArg(narg++, T));
    OCL_CHECK(err, err = kernel.setArg(narg++, D));
    OCL_CHECK(err, err = kernel.setArg(narg++, r));
    OCL_CHECK(err, err = kernel.setArg(narg++, v));
    OCL_CHECK(err, err = kernel.setArg(narg++, M));
    OCL_CHECK(err, err = kernel.setArg(narg++, N));

    uint64_t kernel_start, kernel_end;
    cl::Event event;

    // Launch kernel
    OCL_CHECK(err, err = q.enqueueTask(kernel, NULL, &event));

    // Copy result from device to host
    OCL_CHECK(err, err = q.enqueueMigrateMemObjects({buffer_output}, CL_MIGRATE_MEM_OBJECT_HOST));

    OCL_CHECK(err, err = q.finish());
    delete[] fileBuf;

    OCL_CHECK(err, err = event.getProfilingInfo<uint64_t>(CL_PROFILING_COMMAND_START, &kernel_start));
   
    OCL_CHECK(err, err = event.getProfilingInfo<uint64_t>(CL_PROFILING_COMMAND_END, &kernel_end));

    // Initialise prices at maturity
    if(type_r == 0) {
    	for(int i = 0; i < M; i++) {
    		output[i] = max(output[i] - K, 0);
    	}
    } else {
    	for(int i = 0; i < M; i++) {
    		output[i] = max(K - output[i], 0);
    	}
    }

    DATA_TYPE sum_CT = 0;
    DATA_TYPE sum_CT2 = 0;

    // Calculate standard error and option price
    for(int i = 0; i < M; i++) {
        sum_CT += output[i];
        sum_CT2 += output[i] * output[i];
    }

    DATA_TYPE value = sum_CT / (DATA_TYPE)M * exp(-r * T);
    DATA_TYPE SD = sqrt((sum_CT2 - (sum_CT * sum_CT) / (DATA_TYPE)M) * exp(-2 * r * T) / ((DATA_TYPE)M - 1));
    DATA_TYPE standard_error = SD / sqrt(M);

    // Stop timer
    gettimeofday(&stop, NULL);

    std::cout << std::setprecision(8) << "Option price " << value << "; Standard error " << standard_error << std::endl;
    std::cout << std::setprecision(8) << "Time taken for path generation " << (float)(kernel_end - kernel_start) / 1000000000 << " seconds" << std::endl;
    std::cout << std::setprecision(8) << "Total time taken " << (double) (stop.tv_usec - start.tv_usec) / 1000000 + (double) (stop.tv_sec - start.tv_sec) << " seconds" << std::endl;

    return 0;
}


//#pragma HLS INTERFACE m_axi port=output_r bundle=gmem0
//#pragma HLS INTERFACE s_axilite port=output_r bundle=control
//#pragma HLS INTERFACE s_axilite port=S bundle=gmem1
//#pragma HLS INTERFACE s_axilite port=S bundle=control
//#pragma HLS INTERFACE s_axilite port=K bundle=gmem1
//#pragma HLS INTERFACE s_axilite port=K bundle=control
//#pragma HLS INTERFACE s_axilite port=T bundle=gmem1
//#pragma HLS INTERFACE s_axilite port=T bundle=control
//#pragma HLS INTERFACE s_axilite port=D bundle=gmem1
//#pragma HLS INTERFACE s_axilite port=D bundle=control
//#pragma HLS INTERFACE s_axilite port=r bundle=gmem1
//#pragma HLS INTERFACE s_axilite port=r bundle=control
//#pragma HLS INTERFACE s_axilite port=v bundle=gmem1
//#pragma HLS INTERFACE s_axilite port=v bundle=control
//#pragma HLS INTERFACE s_axilite port=M bundle=control
//#pragma HLS INTERFACE s_axilite port=N bundle=control
//#pragma HLS INTERFACE s_axilite port=return bundle=control
