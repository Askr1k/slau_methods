"""Модуль matrices содержит функции для генерации матриц."""
import numpy as np


def generate_matrix(n, cond):
    """Генерирует матрицу с заданным числом
    обусловленности и диагональным преобладанием."""
    if n < 2 or n % 2 != 0:
        raise ValueError("n должно быть чётным и >= 2")
    if cond <= 1:
        raise ValueError("Число обусловленности должно быть > 1")

    rng = np.random.default_rng()
    m = n // 2

    B = np.zeros((m, m))
    permutation = rng.permutation(m)
    values = rng.uniform(0.5, 2.0, size=m)

    for i in range(m):
        B[i, permutation[i]] = values[i]

    s = np.max(np.abs(B))
    t = s * (cond + 1) / (cond - 1)

    A = np.zeros((n, n))
    A[:m, :m] = t * np.eye(m)
    A[m:, m:] = t * np.eye(m)
    A[:m, m:] = B
    A[m:, :m] = B.T

    return A


if __name__ == "__main__":
    # Параметры
    n = 10
    target_cond = 10000

    # Создание матрицы
    A = generate_matrix(n, target_cond)

    # Вывод матрицы
    print("Матрица:")
    print(A)

    # Проверка размера
    print("\nПроверка размера:")
    print("Размер матрицы:", A.shape)
    print("Матрица квадратная:", A.shape[0] == A.shape[1])

    # Проверка диагонального преобладания
    print("\nПроверка диагонального преобладания:")

    for i in range(n):
        diagonal = abs(A[i, i])
        row_sum = np.sum(np.abs(A[i, :])) - diagonal

        print(
            f"Строка {i + 1}: "
            f"|a_ii| = {diagonal:.6f}, "
            f"сумма остальных элементов = {row_sum:.6f}, "
            f"условие = {diagonal > row_sum}"
        )

    # Проверка невырожденности
    print("\nПроверка невырожденности:")
    print("Ранг матрицы:", np.linalg.matrix_rank(A))
    print("Матрица невырожденная:",
          np.linalg.matrix_rank(A) == n)

    # Проверка числа обусловленности
    print("\nЧисло обусловленности:")
    print(np.linalg.cond(A))
