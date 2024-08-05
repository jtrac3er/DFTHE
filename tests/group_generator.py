"""
generiert alle Elemente einer Gruppe um zu schauen auf Auffälligkeiten

Problem das ich gefunden habe: Wenn man eine Primzahl hat und eine Zerlegung von p-1, 
dann gibt es nicht so viele Zahlen g, die einen kleinen order haben. Also die meisten
Zahlen haben einen Order von p-1, und nur wenige haben einen kleineren. Das ist ein 
Problem für meinen Algorithmus, aber wsl ist das einfach so, und ich habe es nicht gewusst.
Aber das führt dazu, dass der Algorithmus nur einen sehr kleinen Keyspace hat, weil der Keyspace
setzt sich aus der Anzahl solcher Generatoren zusammen

Also: Ich sollte herausfinden, wie ich solche generatoren gut finden kann. Also wenn man einen 
generator hat mit kleinerem Order, dann kann man es einfach potenzieren. Und kleinere werte sind sowieso egal

Also schwanz gegessen, das funktioniert so nicht. Denn:
#elemente g mit ord(g)=n == phi(n)		Wenn n | (p-1)

Also die Anzahl ist konstant und hängt nicht von p ab. Grösseres p bringt also auch nichts. Der KEyspace
ist also sehr klein

Aber ich habe eine neue idee, die auch auf dem nth-root problem beruht. Und zwar ist es schwer,
wenn man p hat, eine n-te Wurzel zu ziehen. Das heisst, es ist schwer, wenn man nur p kennt, eine root of unity
und einen generator zu finden - das heisst, es gibt zwar wenige keys, aber diese sind schwer zu finden. Die 
Sicherheit würde dann einfach aus der randomness im encoding kommen. 

Die Frage ist: Kann man die keys nicht einfach so berechnen? Die Keys bestehen aus meistens maximal 2 werten,
die verschieden angeordnet sind, also sie haben folgnede form:
 [a,0,0,...,b,,0,0.,,,]
wobei
 - |a| = 0
 - |b| = 0

Also es gibt schon genug verschiedene Paare hier, und nur eines ist richtig. Was charakterisiert dann
das richtige Paar?
 - durch herausprobieren habe ich gemerkt, dass
	a + b = (1,0)
	a ^ 2 = a
	b ^ 2 = b
 - und meistens gilt, dass die erste komponente der beiden zahlen gleich ist und die hälfte von p+1 ist.
   Also wie schwer ist es, dazu einen imaginären teil zu finden?

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



"""
def find_good_prime():

	def is_prime(number):
		for i in range(2, int(number**0.5) + 1):
			if number % i == 0:
				return False
		return True

	for i in range(3, 10_000):
		#p = i*(n*2) + 1
		p = i*(n**5) + 1
		if is_prime(p):
			return p
n = 5
p = 37
print("Primzahl: ", p)

def order(x):
	for i in range(1,p):
		if pow(x, i, p) == 1:
			return i

d = {}

for i in range(1,p):
	o = order(i)
	if o in d:
		d[o] += 1
	else:
		d[o] = 1

print(d)

"""

# Dasselbe, aber einfach für Komplexe Zahlen
p = 17
d = {}

def order(x):
	for i in range(1,p**2):
		if pot(x, i) == (1,0):
			return i
	return -1

try:
	for i in range(p):
		for j in range(p):
			rand = (i,j)
			o = order(rand)
			if o in d:
				d[o] += 1
			else:
				d[o] = 1
except KeyboardInterrupt:
	pass

print(d)