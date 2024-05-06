import math
import random


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

# sin taylor series
def sin_(x):
    x = x % (2 * 3.14159265358979323846)
    result = 0
    for i in range(10):
        result += ((-1) ** i) * (x ** (2 * i + 1)) / factorial(2 * i + 1)
    return result


# for i in range(10):
#     arg = random.random() * 10
#     print(f"sin_({arg}) = {sin_(arg)}")
#     print(f"math.sin({arg}) = {math.sin(arg)}")


a = 1 + + + + + - - - -1
print(a)