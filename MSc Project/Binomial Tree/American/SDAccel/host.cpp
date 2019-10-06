#include "xcl2.hpp"
#include <stdlib.h>
#include <vector>
#include <algorithm>

#define MAX_TREE_HEIGHT 30000
#define MIN_TREE_HEIGHT 2
#define MAX_ENTRIES 25
#define DATA_TYPE float

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cout << "Usage: " << argv[0] << " <XCLBIN File>" << std::endl;
        return EXIT_FAILURE;
    }

    std::string binaryFile = argv[1];
    cl_int err;
    unsigned fileBufSize;

    // Allocate memory
    std::vector<DATA_TYPE, aligned_allocator<DATA_TYPE>> host_output(MAX_ENTRIES * sizeof(DATA_TYPE));
    std::vector<DATA_TYPE, aligned_allocator<DATA_TYPE>> device_output(MAX_ENTRIES * sizeof(DATA_TYPE));
    std::vector<DATA_TYPE, aligned_allocator<DATA_TYPE>> S(MAX_ENTRIES * sizeof(DATA_TYPE));
    std::vector<DATA_TYPE, aligned_allocator<DATA_TYPE>> K(MAX_ENTRIES * sizeof(DATA_TYPE));
    std::vector<DATA_TYPE, aligned_allocator<DATA_TYPE>> T(MAX_ENTRIES * sizeof(DATA_TYPE));
    std::vector<DATA_TYPE, aligned_allocator<DATA_TYPE>> D(MAX_ENTRIES * sizeof(DATA_TYPE));
    std::vector<DATA_TYPE, aligned_allocator<DATA_TYPE>> r(MAX_ENTRIES * sizeof(DATA_TYPE));
    std::vector<DATA_TYPE, aligned_allocator<DATA_TYPE>> v(MAX_ENTRIES * sizeof(DATA_TYPE));
    std::vector<int, aligned_allocator<int>> type(MAX_ENTRIES * sizeof(int));
    std::vector<int, aligned_allocator<int>> height(MAX_ENTRIES * sizeof(int));
    int num_options = 0;

    // Load data from text file
    FILE* file = fopen("../option_data.txt", "r");
    char linebuf[512];

    // Check that the data file was read
    if (file == NULL) {
        std::cout << "[ERROR] Unable to open data file" << std::endl;
        exit(0);
    }

    // Read the data
    while(fgets(linebuf, sizeof(linebuf), file) != NULL) {
        if(num_options >= 25) {
        	std::cout << "[WARNING] Reached maximum number of options" << std::endl;
            break;
        }

        // Skip hashtags and new lines
        if(linebuf[0] == '#' || linebuf[0] == '\n') {
            continue;
        }

        // Allocate data to arrays
        sscanf(linebuf, "%f,%f,%f,%f,%f,%f,%d,%d", &S[num_options], &K[num_options], &T[num_options], &D[num_options], &r[num_options], &v[num_options], &type[num_options], &height[num_options]);

        num_options++;
    }

    std::cout << "[SUCCESS] Loaded data for " << num_options << " options" << std::endl;

    for(int i = 0; i < num_options; i++) {
        // Check if MAX_TREE_HEIGHT is exceeded
        if(height[i] > MAX_TREE_HEIGHT) {
            height[i] = MAX_TREE_HEIGHT;
        } else if(height[i] < MIN_TREE_HEIGHT) {
            height[i] = MIN_TREE_HEIGHT;
        }

        std::cout << "[" << i << "] S " << S[i] << "; K " << K[i] << "; T " << T[i] << "; D " << D[i] << "; r "
                  << r[i] << "; v " << v[i] << "; type " << type[i] << "; steps " << height[i] << std::endl;
    }

    fclose(file);

    for(int i = 0; i < num_options; i++) {
    	device_output[i] = 0;
    }

    // Find Xilinx platforms and return a list of devices
    auto devices = xcl::get_xil_devices();
    auto device = devices[0];

    OCL_CHECK(err, cl::Context context(device, NULL, NULL, NULL, &err));
    OCL_CHECK(
        err,
        cl::CommandQueue q(context, device, CL_QUEUE_PROFILING_ENABLE, &err));

    // Read in binary file
    auto fileBuf = xcl::read_binary_file(binaryFile, fileBufSize);
    cl::Program::Binaries bins{{fileBuf, fileBufSize}};

    devices.resize(1);
    OCL_CHECK(err, cl::Program program(context, devices, bins, NULL, &err));
    OCL_CHECK(err, cl::Kernel kernel(program, "binomial_tree", &err));

    // Allocate buffers in global memory
    OCL_CHECK(err,
              cl::Buffer buffer_output(context,
                                    CL_MEM_USE_HOST_PTR | CL_MEM_READ_ONLY,
                                    MAX_ENTRIES * sizeof(DATA_TYPE),
                                    device_output.data(),
                                    &err));
    OCL_CHECK(err,
              cl::Buffer buffer_S(context,
                                    CL_MEM_USE_HOST_PTR | CL_MEM_READ_ONLY,
                                    MAX_ENTRIES * sizeof(DATA_TYPE),
                                    S.data(),
                                    &err));
    OCL_CHECK(err,
              cl::Buffer buffer_K(context,
                                       CL_MEM_USE_HOST_PTR | CL_MEM_WRITE_ONLY,
                                       MAX_ENTRIES * sizeof(DATA_TYPE),
                                       K.data(),
                                       &err));
    OCL_CHECK(err,
              cl::Buffer buffer_T(context,
                                    CL_MEM_USE_HOST_PTR | CL_MEM_READ_ONLY,
                                    MAX_ENTRIES * sizeof(DATA_TYPE),
                                    T.data(),
                                    &err));
    OCL_CHECK(err,
              cl::Buffer buffer_D(context,
                                       CL_MEM_USE_HOST_PTR | CL_MEM_WRITE_ONLY,
                                       MAX_ENTRIES * sizeof(DATA_TYPE),
                                       D.data(),
                                       &err));
    OCL_CHECK(err,
              cl::Buffer buffer_r(context,
                                    CL_MEM_USE_HOST_PTR | CL_MEM_READ_ONLY,
                                    MAX_ENTRIES * sizeof(DATA_TYPE),
                                    r.data(),
                                    &err));
    OCL_CHECK(err,
              cl::Buffer buffer_v(context,
                                       CL_MEM_USE_HOST_PTR | CL_MEM_WRITE_ONLY,
                                       MAX_ENTRIES * sizeof(DATA_TYPE),
                                       v.data(),
                                       &err));

    OCL_CHECK(err,
              cl::Buffer buffer_type(context,
                                       CL_MEM_USE_HOST_PTR | CL_MEM_WRITE_ONLY,
                                       MAX_ENTRIES * sizeof(int),
                                       type.data(),
                                       &err));

    OCL_CHECK(err,
              cl::Buffer buffer_height(context,
                                       CL_MEM_USE_HOST_PTR | CL_MEM_WRITE_ONLY,
                                       MAX_ENTRIES * sizeof(int),
                                       height.data(),
                                       &err));

    OCL_CHECK(err, err = kernel.setArg(0, buffer_output));
    OCL_CHECK(err, err = kernel.setArg(1, buffer_S));
    OCL_CHECK(err, err = kernel.setArg(2, buffer_K));
    OCL_CHECK(err, err = kernel.setArg(3, buffer_T));
    OCL_CHECK(err, err = kernel.setArg(4, buffer_D));
    OCL_CHECK(err, err = kernel.setArg(5, buffer_r));
    OCL_CHECK(err, err = kernel.setArg(6, buffer_v));
    OCL_CHECK(err, err = kernel.setArg(7, buffer_type));
    OCL_CHECK(err, err = kernel.setArg(8, buffer_height));
    OCL_CHECK(err, err = kernel.setArg(9, num_options));

    // Copy input data to device global memory
    OCL_CHECK(err,
              err = q.enqueueMigrateMemObjects({buffer_S, buffer_K, buffer_T, buffer_D, buffer_r, buffer_v, buffer_type, buffer_height}, 0));

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


    for(int i = 0; i < num_options; i++) {
        std::cout << "[" << i << "] Option price: " << device_output[i] << std::endl;
    }

    std::cout << "Time taken " << (kernel_end - kernel_start) << " nanoseconds" << std::endl;

    return 0;
}
