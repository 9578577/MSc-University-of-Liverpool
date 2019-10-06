# COMP702-FPGA-MSc-Project
An investigation into the usability of FPGAs to accelerate numerical libraries. This repository consists of workings towards the COMP702 module for MSc Big Data &amp; HPC at Uni of Liverpool.

Current implementation performs a MC simulation using 100 paths with 10 steps per path, able to change initial starting conditions. 

TO DO: HLS Streams for MC simulation, create following pipeline

Transfer BS Settings -> Mersenne Twister -> Box Muller -> Path Movements -> Write to Host -> Calculate Option Price
to Device
