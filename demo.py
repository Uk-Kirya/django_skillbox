import time
from functools import cache

@cache
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

def runtime(func):
    def wrapper():
        start = time.time()
        result = func()
        end = time.time()
        print('runtime', end - start)
        return result
    return wrapper

@runtime
def main():
    print(factorial(5))

if __name__ == '__main__':
    main()