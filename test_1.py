import math


def func(x):
    return x


def pow_2(x):
    return x*x


def op_int(f, a, b):
    res = f(a)
    i = 0.001
    while (a < b):
        res = res + f(a)*i
        a = a + i
    return res


a = 0
b = 3
print(op_int(pow_2, a, b))
