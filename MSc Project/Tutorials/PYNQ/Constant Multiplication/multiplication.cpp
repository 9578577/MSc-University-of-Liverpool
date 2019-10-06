/*
 * Tutorial https://pynq.readthedocs.io/en/v2.4/overlay_design_methodology/overlay_tutorial.html
 */

void multiply(int a, int b, int& c) {
#pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS INTERFACE s_axilite port=a
#pragma HLS INTERFACE s_axilite port=b
#pragma HLS INTERFACE s_axilite port=c

    c = a * b;
}