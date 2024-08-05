"""

Die Idee ist, einfach ein Polynom zu nehmen und dann den Geheimcode als Auswertung
dieses Poylnom zu nehmen an einer Unbekannten Stelle. 

Also: Wähle P, sodass P(key) = m

Man wählt einen Ring aus, sodass das Polynom, durch das man teilt einen Teiler
von den Komponenten gibt
"""

import numpy as np
import scipy.linalg

p = 7	# q
q = 5	# p
d = 3 	# grad des polynomrings
k = 10	# geheimer key

N = p * q	# Körper/Halbkörper (weil nicht prim) über welchem das polynom ist
			# also der komponenten Modulus

# Also: Zuerst brauche ich mal ein Paar primitive, denn numpy macht das ganze nicht 
# ich brauche manuelle Polynomdivision

def finiteFieldInverse(x):
	return (x ** ((p-1)*(q-1) -1)) % N

def trailingOne(i):
	z = np.zeros(i+1, dtype=int)
	z[i] = 1
	return z

# Teile a durch b und gebe resultat und Rest aus
def polyDiv(a,b):
	order_a = len(a)
	order_b = len(b)
	sol = np.zeros(order_a - order_b, dtype=int)
	for i in range(order_a - order_b + 1):
		highest_coeff_a = a[i]
		highest_coeff_b = b[0]

		# so: nun muss ich x = a / b, sodass a = bx | hierzu muss ich b^-1 berechnen
		x = (finiteFieldInverse(highest_coeff_b) * highest_coeff_a) % N

		# Das kann man nun hinzufügen für die Lösung
		trail = trailingOne()
		a -= np.polymul(b * x, trail) 
		sol += np.polymul(x, trail)

		print(order_a, order_b, highest_coeff_a, highest_coeff_b, x, a, b, sol)
	return sol,a


x = np.array([3,3,1], dtype=int)
y = np.array([1,0], dtype=int)
print(polyDiv(x,y))