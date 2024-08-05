"""
Also hier eine verallgemeinerte Form von der Conv-FHE
"""

from functools import reduce
from random import randint
from tsroot import *


n = 3
p = 191 #find_good_prime()
d = []

encoding_len = n // 2
print(f"Die Primzahl ist {p}!")

"""
Support Funktionen für Komplexe Zahlen
"""

def mul(x,y):
	return ((x[0]*y[0] - x[1]*y[1]) % p, (x[0]*y[1] + x[1]*y[0]) % p)

def add(x,y):
	return ((x[0]+y[0]) % p, (x[1]+y[1]) % p)

def t(x):
	return (x[0], (-x[1]) % p)

def l(x):
	return (x[0]**2 + x[1]**2) % p

def pot(x,n):
	res = (1,0)
	for i in range(n):
		res = mul(res, x)
	return res

def matrix_mul(A,x):
	result = [(0,0) for i in range(n)]
	for i in range(n):
		for j in range(n):
			result[i] = add(result[i], mul(A[i][j], x[j]))
	return result


"""
Support funktionen für DFT
"""

unity_root = None

def get_unity_root():
	global unity_root
	if unity_root:
		return unity_root

	while True:
		rand = (randint(0,p-1), randint(0,p-1))
		scale = root(inv(l(rand)))
		if scale == -1:
			# no root founds
			continue
		rand = ((scale*rand[0]) % p, (scale*rand[1]) % p)
		if l(rand) == 1 and pot(rand, n) == (1,0):
			print(rand, l(rand), pot(rand, n))
			found = True
			for i in range(1, n-1):
				if pot(rand, i) == (1,0):
					found = False
					break
			if found:
				unity_root = rand
				return rand 


def create_dft_matrices():
	m = [[0 for i in range(n)] for i in range(n)]
	m_inv = m
	unity_root = get_unity_root()
	for i in range(n):
		for j in range(n):
			scale = (inv(n), 0)
			m[i][j] = pot(unity_root, i*j)
			m[i][j] = mul(m[i][j], scale)

	for i in range(n):
		for j in range(n):
			m_inv[i][j] = t(m[i][j])

	return (m, m_inv)


def get_generator():
	while True:
		rand = (randint(0, p-1), randint(0, p-1))
		#rand = (randint(0, p-1), 0)
		if pot(rand, n) == (1, 0):
			return rand 
	raise ValueError("Could not find generator")


# Viele keys sind einfach schlecht und unsicher
def check_good_key(key):
	if (1,0) in key:
		return False

	if n % 2 == 0:
		for k in range(2):
			bad_shift = True
			for i in range(encoding_len):
				bad_shift &= (key[i*2 + k] == (0,0))
			if bad_shift:
				return False

	return True


def create_keys():
	while True:
		g = get_generator()
		m, m_inv = create_dft_matrices()
		k = [pot(g, i) for i in range(n)]
		k_inv = scalar_mul(k[::-1], g)
		key =  matrix_mul(m_inv, k)
		key_inv = matrix_mul(m_inv, k_inv)
		print(k)

		if not check_good_key(key):
			continue
		return key, key_inv


"""
Weitere Support Funktionen
"""

def pw_mul(v,w):
	return [mul(x,y) for x,y in zip(v,w)]

def pw_add(v,w):
	return [add(x,y) for x,y in zip(v,w)]

def pw_pow(v, n):
	res = [(1,0) for i in range(n)]
	for i in range(n):
		res = pw_mul(res, v)
	return res

def convolve(v,w):
	result = [(0,0) for i in range(n)]
	for i in range(n):
		for j in range(n):
			result[(i+j) % n] = add(result[(i+j) % n], mul(v[i], w[j]))
	return result

def inv(x):
	return pow(x, p-2, p)

def root(x):
	return STonelli(x, p)

def scalar_mul(vec, k):
	return pw_mul(vec, [k for i in range(n)])

def encode(m):
	l = []
	for i in range(encoding_len):
		l.append((m,0))
		l.append((randint(0,p-1), randint(0, p-1)))
	if n % 2 == 1:
		l.append((m,0))
	return l

def decode(e):
	for i in range(encoding_len):
		if not e[0] == e[i*2] or (n % 2 == 1 and not e[-1] == e[0]):
			raise ValueError("Error decode - not same number")
	if e[0][1] != 0:
		raise ValueError("Error decode - imaginary part not zero")
	return e[0][0]

def encrypt(m, k):
	return convolve(encode(m), key)

def decrypt(c, k_inv):
	return decode(convolve(c, key_inv))

def hom_mul(c1, c2):
	return pw_mul(c1, c2)

def hom_add(c1, c2):
	return pw_add(c1, c2)

def to_len(s):
	return [l(e) for e in s]


# Also: nun beginnt der Spass
key, key_inv = create_keys()
print("K:\t", key)
print("K^-1:\t", key_inv)
print()

n1 = 5
n2 = 10
m1 = encrypt(n1, key)
m2 = encrypt(n2, key)
print(f"{n1}:\t", m1)
print(f"{n2}:\t", m2)
print()

m_add = hom_add(m1, m2)
m_mul = hom_mul(m1, m2)
print(f"{n1}+{n2}:\t", m_add)
print(f"{n1}*{n2}:\t", m_mul)
print()
print(decrypt(m_add, key_inv))
print(decrypt(m_mul, key_inv))

