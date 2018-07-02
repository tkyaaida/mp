
EPSILON = 1e-8


def newton(f_prime, f_prime2, x):
    i = 0
    while True:
        i += 1
        x_new = x - f_prime(x) / f_prime2(x)
        print(f'{i}: x = {x_new}')
        if abs(x_new - x) < EPSILON:
            break
        x = x_new
    return x_new
