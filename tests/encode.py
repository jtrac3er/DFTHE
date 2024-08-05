"""
Das encoding geht auch ganz einfach. Ich brauche nur genug gute zahlen

"""

k1 = 431
k2 = 7

k = k1 * k2
m1 = -1
m2 = -1
r = 4

for x in range(2, k1):
	if (x*k2) % k1 == 1: 
		m1 = (x*k2) % k
		break

for x in range(2, k2):
	if (x*k1) % k2 == 1: 
		m2 = (x*k1) % k
		break
		

if m1 == -1: raise ValueError("kein wert gefunden für m1")
if m2 == -1: raise ValueError("kein wert gefunden für m2")

def encode(d):
	return (d*m1 + r*m2) % k 

def decode(e):
	return e % k1

d1 = 12
d2 = 9

e1 = encode(d1)
e2 = encode(d2)

e_mul = (e1 * e2) % k 
e_add = (e1 + e2) % k 

d_mul = decode(e_mul)
d_add = decode(e_add)


print(f"d1={d1};e1={e1}, d2={d2};e2={e2} || e_mul={e_mul};d_mul={d_mul}, e_add={e_add};d_add={d_add}")

