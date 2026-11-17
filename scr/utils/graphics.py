"""Модуль graphics содержит функции для создания
графиков по результатам исследований
"""
import matplotlib.pyplot as plt
MARKERS = ['o-', 's-', '^-']


def make_graphic_time(data):
    """Возвращает график зависимости времени
    выполнения метода от размера матрицы"""
    fig, ax = plt.subplots(figsize=(9, 5))
    for (arrx, arry, title), mark in zip(data, MARKERS):
        ax.plot(arrx, arry, mark, label=title)
    ax.set_xlabel('Размер матрицы N')
    ax.set_ylabel('Время, c')
    ax.set_title('Зависимость времени выполнения от размера матрицы')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()
    return fig


def make_graphic_time_lang(data_f, data_p):
    """Возвращает график зависимости времени
    выполнения метода от размера матрицы"""
    fig, ax = plt.subplots(figsize=(9, 5))
    for (arrx, arry, title), mark in zip(data_f, MARKERS):
        ax.semilogy(arrx, arry, mark, label=title + 'на Fortran',
                    color="#CB18E7")
    for (arrx, arry, title), mark in zip(data_p, MARKERS):
        ax.semilogy(arrx, arry, mark, label=title + 'на Python',
                    color="#0D97ED")
    ax.set_xlabel('Размер матрицы N')
    ax.set_ylabel('Время, c')
    ax.set_title('Зависимость времени выполнения от размера матрицы')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()
    return fig


def make_graphic_err(data, title_h):
    """Возвращает график зависимости погрешностей или
    нормы невязки от числа обусловленности"""
    fig, ax = plt.subplots(figsize=(9, 5))
    for (arrx, arry, title), mark in zip(data, MARKERS):
        ax.loglog(arrx, arry, mark, label=title)
    ax.set_xlabel('Число обусловленности')
    ax.set_ylabel(title_h[1])
    ax.set_title(f'Зависимость {title_h[0]} от числа обусловленности')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()
    return fig


def make_graphic_eps_seidel(EPS, rel_err):
    """Возвращает график зависимости точности от
    фактической погрешности для метода Зейделя"""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.loglog(EPS, rel_err, 'o-')
    ax.set_xlabel('Точность eps')
    ax.set_ylabel('Фактическая погрешность')
    ax.set_title('Зависимость фактической погрешности\n'
                 'от точности для метода Зейделя')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()
    return fig
