"""
Also ziel ganz einfach. Ich will überprüfen ob es ein a gibt in einer gruppe K mod z, wobei z = p*q ist, wo gilt
 a^2 = a

Hierzu wird einfach ein bisschen gebruteforcet
"""

def generatePrimes(low, high):
    for i in range(low, high):
        for num in range(2, i):
            if i % num == 0:
                break
        else:
            yield i


for p in generatePrimes(1000, 4000):
	for q in generatePrimes(1000, 4000):
		
		if p == q: continue
		z = p*q

		for a in range(2, z):
			
			a_squared = (a**2) % p
			if a_squared == a % p:
				print(f"Passende Gruppe gefunden: p={p}, q={q}, a={a}\n")

