"""
Neue Idee für eine FHE Verschlüsselung

Primzahlen: 13, 17, 19, 23, 29, 73, 79, 83, 89

"""

p = 29
q = 23
M = (p-1)*(q-1)
G = p*q
Z = p*q*M 

r = 3
g = r*M + 1

for i in range(1, Z):
	if i % M == 0 and i % G == 1:
		M0G1 = i
	if i % M == 1 and i % G == 0:
		M1G0 = i 

def enc(m):
	return ( (m*M1G0 + M0G1) * (g**m) ) % Z

def dec(c):

	def log(b, n, mod):
		for i in range(1, mod):
			if (b**i) % mod == n:
				return i 
		return -1

	return log(g, c % G, G)

def add(x, y):
	return (x * y) % Z 

def mul(x, y):
	return (x ** y) % Z

def sub(x, y):
	return add(x, )


m1 = 2
m2 = 14

c1 = enc(m1)
c2 = enc(m2)

c_mul = mul(c1, c2)
c_add = add(c1, c2)

m_mul = dec(c_mul)
m_add = dec(c_add)

print(f"m1={m1};c1={c1}, m2={m2};c2={c2} || c_mul={c_mul};m_mul={m_mul}, c_add={c_add};m_add={m_add}")

