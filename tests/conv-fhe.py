"""
Support für die  DFT

Imaginäre Zahlen als Tupel

"""

p = 13	#12 = 2*2*3
n = 4

def mul(x,y):
	return ((x[0]*y[0] - x[1]*y[1]) % p, (x[0]*y[1] + x[1]*y[0]) % p)

def add(x,y):
	return ((x[0]+y[0]) % p, (x[1]+y[1]) % p)

def t(x):
	return (x[0], (-x[1]) % p)

def pow(x,n):
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

# nun kann ich auch wurzeln definieren. Hier definiere ich sie für n=4,a also eine 4. Wurzel
# (0, 1) (12, 0) (0, 12) (1, 0)
unity_root = (0, 1)

def create_dft_matrix():
	m = [[0 for i in range(n)] for i in range(n)]
	for i in range(n):
		for j in range(n):
			m[i][j] = pow(unity_root, i*j)

			# dazu muss man aber noch den Faktor von 1/sqrt(n) nehmen
			# also n = 4, sqrt(4) = 2, 2^-1 = 7 (mod 13)
			# aber es gibt hier noch mehr, sqrt(4) = -2 = 11, 11^-1 = 6
			scale = (7,0)
			m[i][j] = mul(m[i][j], scale)

	return m

def create_inv_dft_matrix():
	# hierzu alles transponieren
	m = create_dft_matrix()
	for i in range(n):
		for j in range(n):
			m[i][j] = t(m[i][j])
	return m

def pretty_print_matrix(m):
	for l in m:
		print(l)


dft_matrix = create_dft_matrix()
inv_dft_matrix = create_inv_dft_matrix()
#pretty_print_matrix(create_dft_matrix())

# gut, das funktioniert nun ziemlich gut. Nun kann man zu fft kommen
def jft(v):
	return matrix_mul(dft_matrix, v)

def ijft(v):
	return matrix_mul(inv_dft_matrix, v)

test = [(1,0), (4,0), (7,0), (0,0)]
print(jft(test))
print(ijft(jft(test)))
# funktioniert alles, perfekt

def pw_mul(v,w):
	return [mul(x,y) for x,y in zip(v,w)]

def pw_add(v,w):
	return [add(x,y) for x,y in zip(v,w)]

def convolve(v,w):
	result = [(0,0) for i in range(n)]
	for i in range(n):
		for j in range(n):
			result[(i+j) % n] = add(result[(i+j) % n], mul(v[i], w[j]))
	return result

def inv(z):
	return (z**11) % 13

def scalar_mul(vec, k):
	return pw_mul(vec, [k for i in range(n)])

t1 = [(1,0), (4,0), (7,0), (0,0)]
t2 = [(0,0), (1,0), (1,0), (0,0)]
f1 = jft(t1)
f2 = jft(t2)
res_mul = pw_mul(f1, f2)
res_add = pw_add(f1, f2)
res_con = convolve(f1, f2)
print("convolve: ", ijft(res_mul), convolve(t1, t2))
print("add: ", ijft(res_add), pw_add(t1, t2))
print("mul: ", ijft(res_con), pw_mul(t1, t2))
print(f1, f2)

"""
So nun: Also die diskrete FT über einem Körper funktioniert wirklich, und es ist genial
Irgendwo habe ich aber wsl noch einen kleinen Fehler drin, denn die Faktoren stimmen nicht
ganz überein, aber davon abgesehen funktioniert alles

Nun zum ganzen: Also nun geht es darum, A zu finden

welche Zahl hat ord(g) = 4 in Z13?

Das sind die zahlen und ihre ordnung
1 1
2 12
3 3
4 6
5 4
6 12
7 12
8 4
9 3
10 6
11 12
12 2

"""

# 5 hat ord(5) = 4
A = [(1,0), (5,0), (12,0), (8,0)]
A_conv = convolve(A, A)
A_scaled = scalar_mul(A_conv, (inv(4), 0))
print( A_scaled )

# A muss ein bisschen angepasst werden, 7 = sqrt(4)^-1. 
A = scalar_mul(A, (7,0))

# ja das stimmt sogar echt! Somit muss ich es nur noch durch die IFFT jagen und dann habe ich A
key = ijft(A)
key_inv = ijft(scalar_mul(A[::-1], (5,0)))
print(pw_mul(A, scalar_mul(A[::-1], (5,0))))
print(convolve(key, key_inv))

def encrypt(m):
	e = [(i,0) for i in m]
	return convolve(e, key)

def decrypt(c):
	e = convolve(c, key_inv)
	return [a for (a,b) in e]

def hom_mul(c1, c2):
	return pw_mul(c1, c2)

def hom_add(c1, c2):
	return pw_add(c1, c2)

m1 = [1,2,3,4]
m2 = [0,0,1,0]
c1 = encrypt(m1)
c2 = encrypt(m2)
res_add = hom_add(c1, c2)
res_mul = hom_mul(c1, c2)
print(decrypt(res_add))
print(decrypt(res_mul))

print()
print(c1, c2)

# Und es funktoniert einfach alles perfekt!!! Hurra! 
# Mal abgesehen von den Vorfaktoren, die stimmen teils nicht ganz

# Die Frage ist nur wie sicher ist das ganze
# Also bis jetzt sehe ich ein einziges Problem, und zwar, dass Vektoren wie [1,0,0,0]
# wenn sie verschlüsselt werden auf [a,0,b,0] abgebildet werden, also dass diese Vektoren
# möglicherweise viele Nullstellen haben, aber das ist egal, wenn man es richtig encodet
# dann kann man dies möglicherweise beheben

