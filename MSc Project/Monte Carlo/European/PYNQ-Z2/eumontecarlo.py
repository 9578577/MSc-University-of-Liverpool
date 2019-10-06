from pynq import DefaultIP
from pynq import Overlay
from pynq import Xlnk
import numpy as np
import datetime
import math

class MonteCarloDriver(DefaultIP):
    def __init__(self, description):
        super().__init__(description=description)

    bindto = ['xilinx.com:hls:eu_monte_carlo:1.0']

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
    def M(self):
        return self.read(0x50)
    
    @M.setter
    def M(self, value):
        self.write(0x50, value)
        
    @property
    def N(self):
        return self.read(0x58)
    
    @N.setter
    def N(self, value):
        self.write(0x58, value)

# Load bitstream
t0 = datetime.datetime.now()
overlay = Overlay("./overlay/monte_carlo_euro.bit")
MonteCarlo = overlay.monte_carlo
t1 = datetime.datetime.now()

# Time taken in seconds
delta = t1 - t0
print("Time taken to load bitstream (seconds) " + str((delta.microseconds / 1000000) + delta.seconds))

# Allocate memory for variables
xlnk = Xlnk()
S = xlnk.cma_array(shape=(1), dtype=np.float32)
K = xlnk.cma_array(shape=(1), dtype=np.float32)
T = xlnk.cma_array(shape=(1), dtype=np.float32)
D = xlnk.cma_array(shape=(1), dtype=np.float32)
r = xlnk.cma_array(shape=(1), dtype=np.float32)
v = xlnk.cma_array(shape=(1), dtype=np.float32)

# Set constants
S[0] = 50
K[0] = 50
T[0] = 1
D[0] = 0
r[0] = 0.05
v[0] = 0.20
type_r = 1
M = 100
N = 100
output = xlnk.cma_array(shape=(M), dtype=np.float32)

# Define status codes
ap_start = 1
ap_done = 2
ap_idle = 4
ap_ready = 8

# Transfer data to FPGA
MonteCarlo.output = output.physical_address
MonteCarlo.spot_price = S.physical_address
MonteCarlo.strike_price = K.physical_address
MonteCarlo.time_to_maturity = T.physical_address
MonteCarlo.dividend_yield = D.physical_address
MonteCarlo.risk_free_rate = r.physical_address
MonteCarlo.volatility = v.physical_address
MonteCarlo.type_r = type_r
MonteCarlo.M = M
MonteCarlo.N = N

t0 = datetime.datetime.now()
status = 0

# Run IP on FPGA
if (MonteCarlo.status == ap_idle) or (MonteCarlo.status == ap_ready):
    MonteCarlo.status = ap_start
    
    while(status != ap_idle):
        status = MonteCarlo.status

t1 = datetime.datetime.now()

# Time taken in seconds
delta = t1 - t0
print("Time taken to create paths (seconds) " +  str((delta.microseconds / 1000000) + delta.seconds))

t0 = datetime.datetime.now()
# Determine Option Price
if(type_r == 0):
    for i in range(M):
        output[i] = max(output[i] - K[0], 0)
else:
    for i in range(M):
        output[i] = max(K[0] - output[i], 0)

# Calculate the standard error
sum_CT = 0
sum_CT2 = 0

for i in range(M):
    sum_CT += output[i]
    sum_CT2 += output[i]
    
# Calculate standard deviation
# sd = math.sqrt((sum_CT2 - (sum_CT * sum_CT) / M) * math.exp(-2 * r * T) / (M - 1))

print("Option value ", (sum_CT / M * math.exp(-r * T)))

t1 = datetime.datetime.now()
delta = t1 - t0

# print("Standard deviation ", sd)
print("Time taken to calculate option value " + str((delta.microseconds / 1000000) + delta.seconds))