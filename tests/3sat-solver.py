"""

Eine Idee, um 3-SAT zu lösen und somit P=NP zu beweisen

"""
from functools import reduce
from random import randint

# Also: Das Experiment hat 4 Bits und eine gewisse Tiefe


# Die p und q Moduli, alle sind gegenseitig prim
p = [167, 173, 179, 181]
q = [191, 193, 197, 199]
Z = reduce(lambda x,y: x*y, p + q, 1)
phi = reduce(lambda x,y: x*(y-1), p + q, 1)
lp = 211
sp = 50

# generiere die Bits, welche die Bedinungen erfüllen
B = []
for i in range(4):
	allZeroP = reduce(lambda x,y: x*y, p, 1)
	factorsQ = reduce(lambda x,y: x*y, q, 1) // q[i]
	bit = allZeroP * factorsQ * randint(1, 150)
	assert(bit % q[i] != 0)
	assert(bit % p[i] == 0)
	B.append(bit)


# soll das resultat erzeugen
def extract(x):
	result = []
	for i in range(4):
		bZero = (x % p[i] == 0)
		bOne = (x % q[i] == 0)
		#if (bZero ^ bOne): print("Kollision bei: " + str(i))
		assert(bZero ^ bOne)
		if bZero:
			result.append(0)
		else:
			result.append(1)
	return result

# soll alle variationen durchgehen und diese auswerten
# also schauen, was die gleichung für alle möglichen Bitkombinatinen ergibt
def check(x):
	for i in range(2**4):
		mod = 1
		mod *= q[3] if i & (0b1 << 0) else p[3]
		mod *= q[2] if i & (0b1 << 1) else p[2]
		mod *= q[1] if i & (0b1 << 2) else p[1]
		mod *= q[0] if i & (0b1 << 3) else p[0]

		res = (x % mod) != 0
		print(f"Für die Bitfolge {format(i,'#06b')} ist das Resultat der Gleichung {res}")



# Berechne AND in parallel
def AND(x,y):
	return (x * y * randint(75, 150)) % Z

def OR(x,y):
	return (x + y) % Z

def NOT(x):
	# square and multiply algorithmus
	def sqam(bas, exp, N):
		if (exp == 0):
			return 1;
		if (exp == 1):
			return bas % N;
		 
		t = sqam(bas, int(exp / 2), N);
		t = (t * t) % N;
	
		if (exp % 2 == 0):
			return t;
		else:
			return ((bas % N) * t) % N;

	i = sqam((x + 1), lp, Z)
	j = sqam((i - 1), phi, Z)
	res = ((j - 1) * sp) % Z
	return res

# Nun kann man die gewünschte Funktion berechnen, hier eine einfache
# Die Funktion sollte immer 1 geben ausser in einem einzigen Falle
# res = (b1 | b2 | b3 | b4)


#res = OR(B[0], OR(B[1], OR(B[2], B[3])))							#einzige Lösung: [0,0,0,0]
#res = OR(B[0], OR(B[1], B[2]))										#mehrere Lösungen, b3 variabel
#res = OR( OR(B[0], OR(B[1], OR(B[2], B[3]))),  AND(B[2], B[3]) )
#res = NOT(B[0])
#res = OR(B[0], OR(B[1], OR(B[2], NOT(B[3]))))
#res = OR( AND(B[0], AND(B[1], B[2])), B[3]	)
#res = AND(B[0], AND(B[1], AND(B[2], B[3])))

check( B[0] )
#print(extract(res))
#print(B[0], res)


