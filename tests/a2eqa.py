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


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors



max_num = 100_000


try:
    for i in getPrimes(max_num):
        for p in range(100_000):
            if (G := (i**p)) > max_num:
                break

            # G = i^p , i ist die Primzahl, p ist die Potenz

            for a in range(G):

                if a == 1 or a == 0:
                    continue

                if (a**2) % G == a:
                    print(f"Paar gefunden: G={G}, a={a}")
except KeyboardInterrupt:
    print(f"Gestoppt bei: G={G}, a={a}, p={p}, i={i}")