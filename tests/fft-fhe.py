"""
Nochmals eine Idee, welche auf der Diskreten Finiten Fourier Transformation beruht
Ich finde es eben schon eine recht erstaunliche Sache, dass das funktioniert und 
will etwas darauf aufbauen, denn ich denke, das haben sich noch nicht so viele überlegt

Also eine weitere Idee wäre, mehrere Fourier-Matrizen hintereinander anzuwenden, und immer
ein vielfaches von 2. Weil dann hat man eigentlich auch wieder Werte, die man einfach 
multiplizieren kann und addieren und wenn man es zurücktransformiert, sollte es wieder stimmen

Die Sicherheit würde hier davon kommen, dass man die Reihenfolge der FFT-Matrizen nicht kennt. 
Es gibt nicht so viele verschiedene, da wieder dasselbe Problem wie bei den Generatoren auftaucht,
aber die Anzahl Reihenfolgen ist ja n! und deshalb würde das gut skalieren

Aber ich könnte mir gut vorstellen, dass
 - Multiplikation von 2 DFT Matrizen wieder eine DFT Matrix oder sonst was gibt
 - Die Mulitplikation kommutativ ist und es deshalb schlechter skaliert

"""

import itertools
import math
import random


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

def inv(x):
	return pow(x, p-2, p)

def matrix_vec_mul(A,x):
	result = [(0,0) for i in range(n)]
	for i in range(n):
		for j in range(n):
			result[i] = add(result[i], mul(A[i][j], x[j]))
	return result

def matrix_matrix_mul(A,B):
	result = [[(0,0) for i in range(n)] for j in range(n)]
	for i in range(n):
		for j in range(n):
			for k in range(n):
				result[i][j] = add(result[i][j], mul(A[i][k], B[k][j]))
	return result

def mat_pot(A,pot):
	res = [[(1,0) if i == j else (0,0) for i in range(n)] for j in range(n)]
	for i in range(pot):
		res = matrix_matrix_mul(res, A)
	return res


def create_dft_matrices(unity_root):
	m = [[0 for i in range(n)] for i in range(n)]
	m_inv = m
	for i in range(n):
		for j in range(n):
			scale = (inv(n), 0)
			m[i][j] = pot(unity_root, i*j)
			m[i][j] = mul(m[i][j], scale)

	for i in range(n):
		for j in range(n):
			m_inv[i][j] = t(m[i][j])

	return (m, m_inv)


def find_all_unity_roots():

	def check(rand):
		if l(rand) == 1 and pot(rand, n) == (1,0):
			found = True
			for i in range(1, n-1):
				if pot(rand, i) == (1,0):
					found = False
					break
			if found:
				return True
		return False

	res = []
	for i in range(p):
		for j in range(p):
			rand = (i,j)
			if check(rand):
				res.append(rand)

	return res


def pretty_print_matrix(m):
	for l in m:
		print(l)

# erzeugt random permutations auch mit mehreren malen dieselbe Matrix
def random_perm(arr):
	for k in range(math.factorial(len(arr))):
		res = []
		l = arr
		for i in range(len(arr)):
			index = random.randint(0,len(l)-1)
			res.append(l[index])
		yield res


p = 83
n = 7


unity_roots = find_all_unity_roots()
dft_matrices = []
idft_matrices = []
results = []

# Achtung: Zum teil treten dft-idft paare schon in dft_matrices 

for ur in unity_roots:
	dft_matrices.append(create_dft_matrices(ur)[0])
	idft_matrices.append(create_dft_matrices(ur)[1])

#"""

pretty_print_matrix(matrix_matrix_mul(dft_matrices[0], dft_matrices[5]))
exit()

for m in dft_matrices:
	pretty_print_matrix(m)
	print()

#"""

"""
Zählen wie viel verschiedene es gibt
"""

"""
try:
	already_seen = []
	no_distinct_products = 0
	no_roots = len(unity_roots)
	no_total_products = math.factorial(no_roots)
	no_tried = 0

	if no_roots == 0:
		print("No roots found")
		raise ValueError

	for perm in random_perm(dft_matrices):
		res = perm[0]
		no_tried += 1
		for i in range(1,len(perm)):
			res = matrix_matrix_mul(res, perm[i])
		if not res in already_seen:
			already_seen.append(res)
			no_distinct_products += 1

except KeyboardInterrupt:
	print(f"KeyboardInterrupt... tried {no_tried}/{no_total_products}")

except ValueError:
	pass

finally:
	print(f"#roots: {no_roots}, #matrices: {no_total_products}, \
#distinct: {no_distinct_products}")

#"""

