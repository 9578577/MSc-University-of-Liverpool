from pynq import DefaultIP
from pynq import Overlay
from pynq import Xlnk
import numpy as np
import datetime

class BinomialTreeDriver(DefaultIP):
    def __init__(self, description):
        super().__init__(description=description)

    bindto = ['xilinx.com:hls:binomial_tree:1.0']

    @property
    def status(self):
        return self.read(0x00)
    
    @status.setter
    def status(self, value):
        self.write(0x00, value)

    @property
    def output(self):
        return self.read(0x10)

    @output.setter
    def output(self, value):
        self.write(0x10, value)

    @property
    def spot_price(self):
        return self.read(0x18)

    @spot_price.setter
    def spot_price(self, value):
        self.write(0x18, value)

    @property
    def strike_price(self):
        return self.read(0x20)

    @strike_price.setter
    def strike_price(self, value):
        self.write(0x20, value)

    @property
    def time_to_maturity(self):
        return self.read(0x28)

    @time_to_maturity.setter
    def time_to_maturity(self, value):
        self.write(0x28, value)

    @property
    def dividend_yield(self):
        return self.read(0x30)

    @dividend_yield.setter
    def dividend_yield(self, value):
        self.write(0x30, value)
        
    @property
    def risk_free_rate(self):
        return self.read(0x38)

    @risk_free_rate.setter
    def risk_free_rate(self, value):
        self.write(0x38, value)

    @property
    def volatility(self):
        return self.read(0x40)

    @volatility.setter
    def volatility(self, value):
        self.write(0x40, value)

    @property
    def type_r(self):
        return self.read(0x48)
    
    @type_r.setter
    def type_r(self, value):
        self.write(0x48, value)

    @property
    def height(self):
        return self.read(0x50)
    
    @height.setter
    def height(self, value):
        self.write(0x50, value)
        
    @property
    def n_options(self):
        return self.read(0x58)
    
    @n_options.setter
    def n_options(self, value):
        self.write(0x58, value)

# Load bitstream
t0 = datetime.datetime.now()
overlay = Overlay("./overlay/us_binomial_tree.bit")
BinomialTree = overlay.binomial_tree
t1 = datetime.datetime.now()

# Time taken in seconds
delta = t1 - t0
print("Loaded bitstream in (seconds): ", (delta.microseconds / 1000000) + delta.seconds)

# Load option data
option_data = np.loadtxt("option_data.txt", comments="#", delimiter=",", unpack=False)

# Allocate memory
xlnk = Xlnk()
if(option_data.ndim > 1):
    n_options = len(option_data)
    
    if n_options > 25:
        n_options = 25
else:
    n_options = 1

# Allocate memory
output = xlnk.cma_array(shape=(n_options), dtype=np.float32)
S = xlnk.cma_array(shape=(n_options), dtype=np.float32)
K = xlnk.cma_array(shape=(n_options), dtype=np.float32)
T = xlnk.cma_array(shape=(n_options), dtype=np.float32)
D = xlnk.cma_array(shape=(n_options), dtype=np.float32)
r = xlnk.cma_array(shape=(n_options), dtype=np.float32)
v = xlnk.cma_array(shape=(n_options), dtype=np.float32)
type_r = xlnk.cma_array(shape=(n_options), dtype=np.int32)
height = xlnk.cma_array(shape=(n_options), dtype=np.int32)

print("Number of options: ", n_options)

# Read in option data
if(option_data.ndim > 1): # 2 or more options
    for i in range(n_options):
        S[i] = option_data[i][0]
        K[i] = option_data[i][1]
        T[i] = option_data[i][2]
        D[i] = option_data[i][3]
        r[i] = option_data[i][4]
        v[i] = option_data[i][5]
        type_r[i] = option_data[i][6]
        if(option_data[i][7] > 30000):
            height[i] = 30000
        elif(option_data[i][7] < 2):
            height[i] = 2
        else:
            height[i] =  option_data[i][7]
else:                     # 1 option
    S[0] = option_data[0]
    K[0] = option_data[1]
    T[0] = option_data[2]
    D[0] = option_data[3]
    r[0] = option_data[4]
    v[0] = option_data[5]
    type_r[0] = option_data[6]
    if(option_data[7] > 30000):
        height[0] = 30000
    elif(option_data[7] < 2):
        height[i] = 2
    else:
        height[0] = option_data[7]

# Define status codes
ap_start = 1
ap_done = 2
ap_idle = 4
ap_ready = 8

# Transfer data to FPGA
BinomialTree.output = output.physical_address
BinomialTree.spot_price = S.physical_address
BinomialTree.strike_price = K.physical_address
BinomialTree.time_to_maturity = T.physical_address
BinomialTree.dividend_yield = D.physical_address
BinomialTree.risk_free_rate = r.physical_address
BinomialTree.volatility = v.physical_address
BinomialTree.type_r = type_r.physical_address
BinomialTree.height = height.physical_address
BinomialTree.n_options = n_options

t0 = datetime.datetime.now()
status = 0

# Run IP on FPGA
if (BinomialTree.status == ap_idle) or (BinomialTree.status == ap_ready):
    BinomialTree.status = ap_start
    
    while(status != ap_idle):
        status = BinomialTree.status

t1 = datetime.datetime.now()

# Time taken in seconds
delta = t1 - t0
print("Time taken (seconds): ", (delta.microseconds / 1000000) + delta.seconds)
print(output)
