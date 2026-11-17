"""Модуль содержит численные методы (Жордана, Отражения и Зейделя)
реализованные на языке python"""
import math
import numpy as np

MAX_ITER = 200000


def python_jordan(n, a_orig, b_orig):
    """Реализация метода Жордана на python"""
    a = a_orig.copy()
    b = b_orig.copy()
    x = []
    for i in range(n):
        num_max_el = i
        max_el = abs(a[i, i])
        for k in range(i + 1, n):
            if abs(a[k, i]) > max_el:
                max_el = abs(a[k, i])
                num_max_el = k

        if num_max_el != i:
            temp = a[num_max_el, :]
            a[num_max_el, :] = a[i, :]
            a[i, :] = temp

            temp = b[num_max_el]
            b[num_max_el] = b[i]
            b[i] = temp

        for k in range(n):
            if k == i:
                continue
            mult = a[k, i] / a[i, i]
            for j in range(i, n):
                a[k, j] -= mult * a[i, j]
            b[k] -= mult * b[i]
    for i in range(n):
        x.append(b[i] / a[i, i])
    return x


def python_reflection(n, a_orig, b_orig):
    """Реализация метода Отражений на python"""
    a = a_orig.copy()
    b = b_orig.copy()
    x = [0] * n
    for i in range(n - 1):
        omega_t = [[]]
        omega_t[0] = a[i:n, i]
        norma = math.sqrt(sum(omega_t[0] ** 2))
        omega_t[0][0] += norma if omega_t[0][0] > 0 else - norma
        omega_t = np.array(omega_t)
        omega = omega_t.T
        a[i:n, i:n] -= (2 / norma ** 2) * (omega @ (omega_t @ a[i:n, i:n]))
        b[i:n] -= (2 / norma ** 2) * (omega @ (omega_t @ b[i:n]))
    for i in range(n - 1, -1, -1):
        s = 0
        for j in range(i + 1, n):
            s += a[i, j] * x[j]
        x[i] = (b[i] - s) / a[i, i]
    return x


def python_seidel(n, a_orig, b_orig, eps=1e-15):
    """Реализация метода Зейделя на python"""
    a = np.array(a_orig)
    b = np.array(b_orig)
    x = np.zeros(n)
    s = x.copy()
    for k in range(MAX_ITER):
        for i in range(n):
            x[i] = (b[i] - sum(a[i, :] * x) + a[i, i] * x[i]) / a[i, i]
        if max(abs(x - s)) < eps:
            return x
        s = x.copy()
