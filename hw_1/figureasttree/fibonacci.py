def fib(n):
    if n == 1 or n == 0: return n
    mark = -1 if (n < 0 and n % 2 == 0) else 1

    a, b = 0, 1
    for _ in range(abs(n)):
        temp = b
        b = a + b
        a = temp
    return a * mark
