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

def find_all_unity_roots():

	global p

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

def find_all_mul_invariants():
	res = []
	for i in range(p):
		for j in range(p):
			rand = (i,j)
			if pot(rand, 2) == rand:
				res.append(rand)
	return res

def find_all_zero_len():
	res = []
	for i in range(p):
		for j in range(p):
			rand = (i,j)
			if l(rand) == 0:
				res.append(rand)
	return res

def isprime(n):
	for i in range(2 ,int((n**0.5))+1):
		if n % i == 0:
			return False
	return True

def getPrimes(n):
	yield 2
	i = 1
	while i <= n-2:
		i += 2
		if isprime(i):
			yield i

def prime_decomp(n):
	facs = []
	for p in getPrimes(n + 10):
		while True:
			t = 1
			if n % p == 0:
				t += 1
				n //= p 
			else:
				break
		facs.append((p, t))
	return facs


"""
n = 11
for p in getPrimes(10_000):
	print(f"Primzahl {p} ergibt #unity_roots={len(find_all_unity_roots())}")
#"""

"""
for p in getPrimes(10_000):
	print(f"Primzahl {p} ergibt #mul_invariants={len(find_all_mul_invariants())}")

#"""

#"""
for p in getPrimes(10_000):
	zlen = len(find_all_zero_len())
	gsize = p**2 - zlen
	decomp = prime_decomp(gsize)
	print(f"Primzahl {p} ergibt #zerlo_len={zlen}, Group size: {gsize}")
	#print(f"decomp: {decomp}")

#"""

"""
Also mittlerweile verstehe ich den Aufbau der Komplexen Zahlen. Es sieht folgendermassen aus:
Je nachdem giht es Primzahlen p, bei denen es komplexe Zahlen z = a + bi gibt, für die gilt, dass
|z| = 0. In diesem Falle gibt es 2p Zahlen, die nicht in der multiplikativen Gruppe drin sind. Es
gibt also 2 Fälle

 1. Es gibt nur eine Zahl z, für die gilt |z| = 0. Diese ist (0,0)
 		In diesem Falle ist |G| = p^2 - 1
 2. Es gibt eine von (0,0) verschiedene Zahl z, für die gilt, dass |z| = 0.
 		In diesem Falle ist |G| = p^2 - 2p + 1

Das sind die beiden Fälle. Wenn man 2 Primzahlen p und q kombiniert, dann erhält man auch wieder
ene andere Gruppengrösse und so weiter. Sicherheit basiert dann auf der PFZ

Endcoding:
 - m1 | c1 | r1 | n1
   m2 | c2 | r2 | n2

m: Message
c: checksum
r: random
n: Null

problem: Pro Modulo darf es nie vorkommen, dass alle Werte Null sind und die anderen nicht, weil sonst
könnte man die PFZ lösen. Und eine andere Frage ist noch, ob es unsicher wird, wenn nur in einer Spalte
etwas steht. Also wenn etwas steht, was man kennt, dann ist es auch schlecht. 

Wie macht man den Null-test für m1?

Multipliziere mit
 - r1 | 0 | 0 | r'1
   0  | 0 | 0 | r'2
Vergleiche mit
   0 | 0 | 0 | 0
   0 | 0 | 0 | 0


Problem hier: Wenn m1 nicht 0 ist, dann erhält man 
 - N | 0 | 0 | 0
   0 | 0 | 0 | 0

Also man hat einen Vektor, wo eine Zeile o ist und die andere nicht. Das heisst, damit könnte man die
PFZ zerbrechen und das würde die Sicherheit zerstören. Lösung hierfür ist, dass man die Checksums auch
ins Spiel bringen muss. Oder man erweitert den Test, sodass man nur beide Spalten auf 0 testen kann oder
man ignoriert m2 sowieso und setzt m2=0, wobei man die Hälfte der Codes verliert. Nein die einzige 
Nöglichkeit scheint mir zu sein, wenn man die Checksum miteinbezieht, also das würde dann so aussehen:

Multipliziere mit
   r1 | 1 | 0 | r'1
   0  | 1 | 0 | r'2
Vergleiche mit
   0 | c1 | 0 | 0
   0 | c2 | 0 | 0

Weiteres Problem mit der Vektorgrösse 4. Für Komplexe Zahlen gibt es nur eine Möglichkeit, wie man
ein Element mit ord(g) = 4 findet Es gibt genau 2 Elemente, welche dies erfüllen: (0,1) und (0,-1).
Dies ist möglicherweise zu einfach zu finden (aber wsl auch sicher, wenn man die PFZ kennt, aber man
muss ja kein unnötiges Risiko eingehen). Daher wäre der Vorschlag, dass man Vektorgrösse 5 nimmt und 
nochmals 2 messages hinzufügt

Endcoding 5
 - m1 | m'1 | c1 | r1 | n1
   m2 | m'2 | c2 | r2 | n2

"""