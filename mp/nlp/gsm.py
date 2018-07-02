import math


GOLDEN_RATIO = (-1 + math.sqrt(5)) / 2
EPSILON = 1e-8


def gsm(f, alpha, beta):

    lambda1 = GOLDEN_RATIO ** 2 * (beta - alpha) + alpha
    lambda2 = GOLDEN_RATIO * (beta - alpha) + alpha

    # 最初にf(λ1), f(λ2)を評価
    f_lambda1 = f(lambda1)
    f_lambda2 = f(lambda2)

    i = 0
    while abs(beta-alpha) > EPSILON:
        if f_lambda1 < f_lambda2:
            beta = lambda2
            lambda2 = lambda1
            f_lambda2 = f_lambda1  # 使い回す
            lambda1 = GOLDEN_RATIO ** 2 * (beta - alpha) + alpha
            f_lambda1 = f(lambda1)
        else:
            alpha = lambda1
            lambda1 = lambda2
            f_lambda1 = f_lambda2  # 使い回す
            lambda2 = GOLDEN_RATIO * (beta - alpha) + alpha
            f_lambda2 = f(lambda2)
        print(f'{i+1}: alpha: {alpha}, beta: {beta}')
        i += 1

    return alpha, beta
