"""
Untersuchungen, wie diskrete imaginäre Zahlen funktionieren
"""

p = 13	#12 = 2*2*3

for a in range(p):
	for b in range(p):

		if (a**2 + b**2) % p == 1:
			
			x = a 
			y = b
			for i in range(p):
				print((x,y))
				x_n = (a*x - b*y) % p
				y_n = (b*x + a*y) % p
				x = x_n
				y = y_n
				
			print()

# finde order von zahlen
for g in range(p):
	for k in range(1,p):
		if (g**k) % p == 1:
			print(g, k)
			break