"""Основной файл где проводятся исследования"""
import numpy as np
import time
from scr.utils.matrices import generate_matrix
from scr.utils.graphics import (make_graphic_time,
                                make_graphic_err,
                                make_graphic_eps_seidel,
                                make_graphic_time_lang)
from scr.methods.python.methods import (python_jordan,
                                        python_reflection,
                                        python_seidel)
from scr.methods.fortran import (fortran_jordan,
                                 fortran_reflection,
                                 fortran_seidel)

N = 10
COND = [3**(i % 2) * 10**((i - (i % 2)) / 2) for i in range(2, 16)]
SIZE = [100 * i for i in range(1, 11)]
EPS = [10**(-i) for i in range(1, 16)]
X_EXEPT = np.ones(N) * 2
X_NORMA = 2


def time_check(metod, a, b, n=None):
    """Функция для измерения времени работы алгоритмов"""
    start = time.perf_counter()
    metod(a, b) if n is None else metod(n, a, b)
    end = time.perf_counter()
    return end - start


def time_experiment():
    """Исследование времени выполнения методов"""
    time_jordan, time_reflection, time_seidel = [], [], []
    title = ['Метод Жордана', 'Метод отражений', 'Метод Зейделя']
    for size in SIZE:
        a = generate_matrix(size, 1e2)
        b = a @ (np.ones(size) * 2)
        time_jordan.append(time_check(fortran_jordan, a, b))
        time_reflection.append(time_check(fortran_reflection, a, b))
        time_seidel.append(time_check(fortran_seidel, a, b))

    return make_graphic_time([[SIZE, time_jordan, title[0]],
                              [SIZE, time_reflection, title[1]],
                              [SIZE, time_seidel, title[2]]])


def time_lang_experiment():
    """Исследование времени выполнения методов на разных языках"""
    time_jordan_f, time_reflection_f, time_seidel_f = [], [], []
    time_jordan_p, time_reflection_p, time_seidel_p = [], [], []
    title = ['Метод Жордана', 'Метод отражений', 'Метод Зейделя']
    for size in SIZE:
        a = generate_matrix(size, 1e2)
        b = a @ (np.ones(size) * 2)
        time_jordan_f.append(time_check(fortran_jordan, a, b))
        time_reflection_f.append(time_check(fortran_reflection, a, b))
        time_seidel_f.append(time_check(fortran_seidel, a, b))
        time_jordan_p.append(time_check(python_jordan, a, b, size))
        time_reflection_p.append(time_check(python_reflection, a, b, size))
        time_seidel_p.append(time_check(python_seidel, a, b, size))

    return make_graphic_time_lang([[SIZE, time_jordan_f, title[0]],
                                   [SIZE, time_reflection_f, title[1]],
                                   [SIZE, time_seidel_f, title[2]]],
                                  [[SIZE, time_jordan_p, title[0]],
                                   [SIZE, time_reflection_p, title[1]],
                                   [SIZE, time_seidel_p, title[2]]])


def err_experiments():
    """Исследование зависимости абсолютной, относительной погрешностей
    и невязки методов от числа обусловленности матрицы
    """
    title = ['Метод Жордана', 'Метод отражений', 'Метод Зейделя']
    title_h = [['абсолютной погрешности', 'Абсолютная погрешность'],
               ['относительной погрешности', 'Относительная погрешность'],
               ['нормы невязки', 'Норма невязки']]
    title_met = ['jordan', 'reflection', 'seidel']
    errs = [{title_met[i]: np.array([]) for i in range(3)} for _ in range(3)]
    figs = []
    for cond in COND:
        a = generate_matrix(N, cond)
        b = a @ X_EXEPT
        x = [fortran_jordan(a, b), fortran_reflection(
            a, b), fortran_seidel(a, b)]
        for num_method in range(3):
            errs[0][title_met[num_method]] = np.append(
                errs[0][title_met[num_method]],
                np.linalg.norm(x[num_method] - X_EXEPT, ord=np.inf)
            )
            errs[1][title_met[num_method]] = np.append(
                errs[1][title_met[num_method]],
                np.linalg.norm(x[num_method] - X_EXEPT, ord=np.inf) / X_NORMA
            )
            errs[2][title_met[num_method]] = np.append(
                errs[2][title_met[num_method]],
                np.linalg.norm(a @ x[num_method] - b, ord=np.inf)
            )
    for i, error in enumerate(errs):
        data = []
        for num in range(3):
            values = error[title_met[num]]
            mask = values > 0
            data.append([
                np.array(COND)[mask],
                values[mask],
                title[num]
            ])
        figs.append(make_graphic_err(data, title_h[i]))
    return figs


def eps_experiment():
    """Исследование зависимости фактической погрешности
    от заданной точности в методе Зейделя
    """
    err_rel = np.array([])
    a = generate_matrix(N, 1e3)
    b = a @ X_EXEPT
    for eps in EPS:
        x = fortran_seidel(a, b, eps)
        err_rel = np.append(err_rel, np.linalg.norm(x - X_EXEPT, ord=np.inf)
                            / X_NORMA)
    return make_graphic_eps_seidel(EPS, err_rel)
