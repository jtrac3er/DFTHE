"""

Zuerst die unverschlüsselte Version

"""

n = 8		# Anzahl bits
N = 2*n

modShift = 2**N
modRotate = modShift -1
leftShift = 2
leftRotate = 2

#3·5·17·257 --> 2*4*16*256
rightRotate = (2**(2*4*16*256 -1)) % modRotate

def OR(x,y):
	res = 0
	r = x + y + 0b0101_0101_0101_0101					# ????sb??	s ist signifikant, b muss 0 sein

	for i in range(n):
		r = r * leftRotate**(i*2 + 1) % modRotate		# b??????s
		r = r * leftShift**1 % modShift					# ??????s0
		r = r * rightRotate**(i*2 + 2) % modRotate		# ????s0??

	r = r * rightRotate**1 % modRotate					# a0b0c0d0 --> 0a0b0c0d
	return r

# encoded einen Bit-array 
def encode_tuple(t):
	res = 0
	assert(len(t) == n)
	for bit in t:
		res *= 4
		res += bit
	return res


def number_to_list(n):
	return [1 if digit=='1' else 0 for digit in format(n, '#010b')[2:]]


def assert_correctness():
	for i in range(2**n -1):
		for j in range(2**n -1):
			x = encode_tuple(number_to_list(i))
			y = encode_tuple(number_to_list(j))
			if not x | y == OR(x,y):
				print(bin(x),bin(y),bin(OR(x,y)))


"""
Um durch Addition eine Verschlüsslung zu kriegen muss ich eine Zahl finden, die bei
mehrmaligem Addieren immer gleich bleibt. Also am besten wäre eine Zahl a, sodass 
x*a = a gibt. Aber das gibt es halt nicht, weil dann müsste a = 0 sein und das wäre
keine verschlüsselung. Die Nächstbeste Möglichkeit wäre eine Zahl, sodass x*a = {a1,a2,..}
nur eine kleine Menge von verschiedenen Zahlen ergibt. Weil dann kann man Mechanismen 
finden, sodass man das wieder entschlüsseln kann. Aber ich denke die Gleichung x*a = {...}
hat nur schlechte Lösungen, weil die meisten zahlen die das erfüllen wären der Form 0b11..0000 
und diese würden die letzen Bits nicht mehr verschlüsseln (weil n*a = a --> (n-1)*a = 0)
Man müsste also wie einen counter noch zusätzlich führen um das wieder zu entschlüsseln, dann kann
man den key einfach wieder subtrahieren. 
"""

def assert_correctness_add():
	key = 0b0110_1010_0011_1001		# random
	no_ops = 2						# der counter für Operationen wird immer addiert
	bitmask = 0b0101_0101_0101_0101

	for i in range(2**n -1):
		for j in range(2**n -1):
			a = encode_tuple(number_to_list(i))
			b = encode_tuple(number_to_list(j))
			x = (a + key) % modShift
			y = (b + key) % modShift
			sol = OR(x,y) 
			decrypt = (sol - no_ops*key) % modShift
			if not a | b == decrypt:
				print(bin(OR(a,b)), bin(decrypt))


def assert_correctness_mul():
	key = 0b0110_1010_0011_1001		# random
	key_inv = key ** (2**(N-1) -1)	# inverser key mit gruppe

	for i in range(2**n -1):
		for j in range(2**n -1):
			a = encode_tuple(number_to_list(i))
			b = encode_tuple(number_to_list(j))
			x = (a * key) % modShift
			y = (b * key) % modShift
			assert (x * key_inv % modShift == a)
			if not a | b == (OR(x,y) * key_inv) % modShift:
				print(OR(a,b), OR(x,y) * key_inv % modShift)


assert_correctness_add()


