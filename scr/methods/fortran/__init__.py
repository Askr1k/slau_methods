import os
import numpy as np

_DLL_DIRECTORY = os.add_dll_directory(r"D:\mingw64\bin")

from . import jordan
from . import reflection
from . import seidel


def fortran_jordan(A, b):
    """Решение СЛАУ методом Жордана."""
    return jordan.jordan_mod.jordan_solve(A, b)


def fortran_reflection(A, b):
    """Решение СЛАУ методом отражений Хаусхолдера."""
    return reflection.reflection_method.reflection_solve(A, b)


def fortran_seidel(A, b, eps=1e-15):
    """Решение СЛАУ методом Зейделя."""
    return seidel.seidel_method.seidel_solve(A, b, eps)


__all__ = [
    "fortran_jordan",
    "fortran_reflection",
    "fortran_seidel",
]
