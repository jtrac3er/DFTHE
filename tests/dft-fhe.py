"""
Idee: Schauen ob sich DFT für FHE eignet
"""

import numpy as np 
import scipy.ndimage

p1 = np.array([1,0,1,1])
p2 = np.array([1,1,0,1])
shift1P = np.array([0,1,0,0])

r1 = np.fft.fft(p1)
r2 = np.fft.fft(p2)
shift1R = np.fft.fft(shift1P)

print(r1,r2, shift1R)

def convolve(x, y):                                    
	r = np.array([0+0j,0+0j,0+0j,0+0j])
	for i in range(4):
		for j in range(4):
			r[(i+j) % 4] += x[i] * y[j]
	return r

r3 = np.multiply(r1, shift1R)
r4 = convolve(r1,r2)

p3 = np.fft.ifft(r3)
p4 = np.fft.ifft(r4)

print(p3,r4, p4)
print(convolve(p1,p2))