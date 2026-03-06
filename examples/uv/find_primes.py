def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return [n for n in range(2, limit + 1) if is_prime[n]]


if __name__ == "__main__":
    limit = 10_000_000
    primes = sieve_of_eratosthenes(limit)
    print(f"Found {len(primes):,} prime numbers up to {limit:,}")
    print(f"First 10: {primes[:10]}")
    print(f"Last 10:  {primes[-10:]}")
