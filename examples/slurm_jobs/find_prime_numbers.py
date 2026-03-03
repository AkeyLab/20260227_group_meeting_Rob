def is_prime(n):
    divisible = False
    for i in range(2, n-1):
        if n%i == 0:
            divisible = True
            break

    return not divisible


if __name__ == "__main__":
    start = 30_000_000
    end = 30_005_000

    for n in range(start, end):
        if is_prime(n):
            print(f"{n:,} is a prime number")
