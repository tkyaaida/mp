import math
from gsm import gsm
from bm import bm
from newton import newton


def f1(x):
    """問題1"""
    return 1/x + math.exp(x)


def f1_prime(x):
    return -1 / (x**2) + math.exp(x)


def f1_prime2(x):
    return 2 * x ** (-3) + math.exp(x)


def f2(x):
    return math.sin(5*x) + (x-5)**2


def f2_prime(x):
    return 5 * math.cos(5*x) + 2 * (x-5)


def f2_prime2(x):
    return -25 * math.sin(5*x) + 2


if __name__ == '__main__':
    print('問題1')

    print('-------黄金分割法-----------')
    gsm(f1, 0, 10)

    print('-------二分割法----------')
    bm(f1_prime, 0, 10)

    print('---------ニュートン法----------')
    newton(f1_prime, f1_prime2, 5)

    print('問題2')
    print('-------黄金分割法-----------')
    gsm(f2, 0, 15)

    print('-------二分割法----------')
    bm(f2_prime, 0, 12)

    print('---------ニュートン法----------')
    newton(f2_prime, f2_prime2, 4.5)
