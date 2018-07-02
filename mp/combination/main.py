#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np


def greedy(a, b, c):
    """欲張り法

    :param np.array a: 制約条件の左辺の係数
    :param int b: 制約条件の不等式の右辺
    :param np.array c: 目的関数の係数
    :return np.array: 欲張り法による近似解
    """
    value = c / a  # 利用価値
    index_sorted = np.argsort(value)[::-1]  # 利用価値の降順にソートしたindex

    total = 0
    answer = np.zeros(a.shape[0])

    # 利用価値の大きい順に制約条件の値を超える手前までナップザックに入れていく
    for i in index_sorted:
        if total + a[i] > b:
            continue
        else:
            total += a[i]
            answer[i] = 1
    return answer


def solve_relaxation_problem(a, b, c):
    """緩和問題を解く

    :param np.array a: 制約条件の左辺の係数
    :param int b: 制約条件の不等式の右辺
    :param np.array c: 目的関数の係数
    :return np.array: 緩和問題の答え
    """
    value = c / a  # 利用価値
    index_sorted = np.argsort(value)[::-1]  # 利用価値の降順にソートしたindex

    total = 0
    answer = np.zeros(a.shape[0])

    # 高々1つが実数になる
    for i in index_sorted:
        if total + a[i] > b:
            answer[i] = (b - total) / a[i]  # 境界ギリギリが実数になるかも
            break
        else:
            total += a[i]
            answer[i] = 1
    return answer


def solve_sub_problem(a_sub, b_sub, c_sub, c, answer_fix, answer_temp):
    """部分問題を解く

    :param np.array a_sub: 制約条件の係数
    :param int b_sub: 制約条件の値
    :param np.array c_sub: 部分問題の係数
    :param c:
    :param answer_fix:
    :param answer_temp:
    :return np.array: 暫定解
    :return bool: 終端しているかどうか
    """
    print(f'答えの固定部分: {answer_fix}')
    print(f'暫定解: {answer_temp}')
    print(f'暫定値: {answer_temp.dot(c)}')

    if b_sub < 0:
        print('実行可能解をもたないので, ここから先は探索しない')
        return answer_temp, True

    # 緩和問題を解く
    answer_sub_relaxation = solve_relaxation_problem(a_sub, b_sub, c_sub)

    # 答えの先頭部分(答えが固定されている部分)とマージ
    answer_relaxation = np.hstack([answer_fix, answer_sub_relaxation])  # 答えの固定部分と部分問題の緩和問題の解を合わせた解
    answer = np.hstack([answer_fix, answer_sub_relaxation.astype(int)])  # 今回の解
    print(f'上界値: {answer_relaxation.dot(c)}')

    if answer_temp.dot(c) > answer_relaxation.dot(c):
        # この部分問題の上界値が暫定値を超えないので終端
        print('暫定解を超えないので, ここから先は探索しない')
        return answer_temp, True
    else:
        if np.logical_or(answer_relaxation == 1, answer_relaxation == 0).all():
            # 0, 1条件を満たすのでこの部分問題の最適解になっている
            print('0, 1条件を満たすので原問題の解になっている')
            return answer, True
        else:
            print('終端できないので分岐')
            return answer_temp, False


def bb(a, b, c):
    """ナップザック問題を分枝限定法で解く

    :param np.array a: 制約条件の係数
    :param int b: 制約条件の値
    :param np.array c: 目的関数の係数
    :return:
    """
    answer_temp = greedy(a, b, c)

    # スタックに(aの残り, bの残り, cの残り, 答えの先頭部分)という形式で部分問題を登録する
    stack = [(a, b, c, np.array([]))]

    while stack:
        print('------------------------')
        a_sub, b_sub, c_sub, answer_fix = stack.pop()
        answer_temp, terminated = solve_sub_problem(a_sub, b_sub, c_sub, c, answer_fix, answer_temp)
        if not terminated:
            # 終端していないので, もう一段階分岐する
            answer_fix1 = np.hstack([answer_fix, np.array([1])])
            answer_fix2 = np.hstack([answer_fix, np.array([0])])
            stack.append((a_sub[1:], b - answer_fix1.dot(a[:answer_fix1.size]), c_sub[1:], answer_fix1))
            stack.append((a_sub[1:], b - answer_fix2.dot(a[:answer_fix2.size]), c_sub[1:], answer_fix2))
    return answer_temp


if __name__ == '__main__':
    a = np.array([2, 3, 5, 6])  # 制約条件の係数
    b = 9  # 制約条件の値
    c = np.array([4, 5, 12, 14])  # 目的関数の係数

    # 分枝限定法により最適解を求める
    answer = bb(a, b, c)

    print('----------------------------')
    print(f'最適解: {answer}')
    print(f'最適値: {answer.dot(c)}')
