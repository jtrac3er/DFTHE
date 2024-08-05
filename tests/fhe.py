"""
Die Implementation mit einem Python script zuerst mal ohne encoding

"""

a = 274449
p = 1009
q = 1019
k = 6			# jetzt noch nicht so wichtig
r = 3			# a hat schon ein 'r' drin

# aber hier wird berechnet
z = p*q*k

def encrypt(m):
	return (m*(a**r)) % z 

def decrypt(c):
	return (c % p) // (a % p) 

def mul(c1, c2):
	return (c1 * c2) % z

def add(c1, c2):
	return (c1 + c2) % z

m1 = 1000
m2 = 9

c1 = encrypt(m1)
c2 = encrypt(m2)

c_mul = mul(c1, c2)
c_add = add(c1, c2)

m_mul = decrypt(c_mul)
m_add = decrypt(c_add)

print(f"m1={m1};c1={c1}, m2={m2};c2={c2} || c_mul={c_mul};m_mul={m_mul}, c_add={c_add};m_add={m_add}")

