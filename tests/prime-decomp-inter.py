
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
		t = 0
		while True:
			if n % p == 0:
				t += 1
				n //= p 
			else:
				break
		if t > 0:
			facs.append((p, t))
	return facs

i = int(input("Gib die Zahl ein: "))
print(prime_decomp(i))