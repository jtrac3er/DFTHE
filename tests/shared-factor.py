
import math

for i in range(1,100):
	for j in range(1,100):
		x0 = 0*i + j
		x1 = 1*i + j
		x2 = 2*i + j

		for mod in range(1,300):
			if math.gcd(x1,x2) != math.gcd(x1,x0):
				print(i,j)