

EPSILON = 1e-8


def bm(f_prime, alpha, beta):

    lamd = (alpha + beta) / 2

    i = 0
    while abs(beta - alpha) > EPSILON:
        if f_prime(lamd) > 0:
            beta = lamd
        elif f_prime(lamd) < 0:
            alpha = lamd
        print(f'{i+1}: alpha {alpha}, beta: {beta}')
        i += 1

        # lamdの更新
        lamd = (alpha + beta) / 2

    return alpha, beta
