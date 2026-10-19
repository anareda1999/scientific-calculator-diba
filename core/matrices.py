"""
core/matrices.py
================
Matrix operations for the DIDA Scientific Calculator.

Matrices are plain lists of lists of complex numbers.
"""

import math

__all__ = [
    "MatrixError", "identity", "zeros", "transpose", "det", "inverse",
    "matmul", "matadd", "matpow", "trace", "rank", "identity_check",
    "format_matrix",
]


class MatrixError(Exception):
    """Raised for any invalid matrix operation."""


def _check(matrix):
    if not matrix or len(matrix[0]) == 0:
        raise MatrixError("Matrice vide")
    width = len(matrix[0])
    for row in matrix:
        if len(row) != width:
            raise MatrixError("Toutes les lignes doivent avoir la même taille")
    return len(matrix), width


def zeros(rows, cols, value=0):
    return [[complex(value) for _ in range(cols)] for _ in range(rows)]


def identity(n):
    return [[complex(1 if i == j else 0) for j in range(n)] for i in range(n)]


def transpose(matrix):
    rows, cols = _check(matrix)
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]


def det(matrix):
    """Determinant via LU decomposition with partial pivoting."""
    rows, cols = _check(matrix)
    if rows != cols:
        raise MatrixError("Le déterminant nécessite une matrice carrée")
    n = rows
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    work = [[complex(v) for v in row] for row in matrix]
    result = complex(1)
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(work[r][col]))
        if abs(work[pivot][col]) < 1e-14:
            return complex(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result = -result
        result *= work[col][col]
        for row in range(col + 1, n):
            factor = work[row][col] / work[col][col]
            for k in range(col, n):
                work[row][k] -= factor * work[col][k]
    return result


def inverse(matrix):
    """Inverse via Gauss-Jordan elimination."""
    rows, cols = _check(matrix)
    if rows != cols:
        raise MatrixError("L'inverse nécessite une matrice carrée")
    n = rows
    aug = [[complex(v) for v in row] + [complex(1 if i == j else 0)
                                         for j in range(n)]
           for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-14:
            raise MatrixError("Matrice singulière : pas d'inverse")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        div = aug[col][col]
        aug[col] = [v / div for v in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor != 0:
                aug[row] = [aug[row][k] - factor * aug[col][k]
                            for k in range(2 * n)]
    return [row[n:] for row in aug]


def matmul(a, b):
    ra, ca = _check(a)
    rb, cb = _check(b)
    if ca != rb:
        raise MatrixError("Dimensions incompatibles pour le produit")
    return [[sum(a[i][k] * b[k][j] for k in range(ca))
             for j in range(cb)] for i in range(ra)]


def matadd(a, b):
    ra, ca = _check(a)
    rb, cb = _check(b)
    if (ra, ca) != (rb, cb):
        raise MatrixError("Dimensions incompatibles pour la somme")
    return [[a[i][j] + b[i][j] for j in range(ca)] for i in range(ra)]


def matpow(matrix, power):
    rows, cols = _check(matrix)
    if rows != cols:
        raise MatrixError("La puissance nécessite une matrice carrée")
    if power < 0:
        return matpow(inverse(matrix), -power)
    result = identity(rows)
    base = matrix
    while power:
        if power & 1:
            result = matmul(result, base)
        base = matmul(base, base)
        power >>= 1
    return result


def trace(matrix):
    rows, cols = _check(matrix)
    if rows != cols:
        raise MatrixError("La trace nécessite une matrice carrée")
    return sum(matrix[i][i] for i in range(rows))


def rank(matrix):
    """Numerical rank via row reduction."""
    rows, cols = _check(matrix)
    work = [[complex(v) for v in row] for row in matrix]
    r = 0
    for col in range(cols):
        if r >= rows:
            break
        pivot = max(range(r, rows), key=lambda rr: abs(work[rr][col]))
        if abs(work[pivot][col]) < 1e-12:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        for row in range(rows):
            if row != r and work[row][col] != 0:
                factor = work[row][col] / work[r][col]
                for k in range(col, cols):
                    work[row][k] -= factor * work[r][k]
        r += 1
    return r


def identity_check(matrix):
    """Return True when the matrix is the identity matrix."""
    rows, cols = _check(matrix)
    if rows != cols:
        return False
    for i in range(rows):
        for j in range(cols):
            expected = complex(1 if i == j else 0)
            if abs(matrix[i][j] - expected) > 1e-12:
                return False
    return True


def format_matrix(matrix, precision=6):
    """Return a printable multi-line string for a matrix."""
    from .engine import format_number
    rows, cols = _check(matrix)
    cells = [[format_number(v, precision) for v in row] for row in matrix]
    widths = [max(len(cells[r][c]) for r in range(rows)) for c in range(cols)]
    lines = []
    for r in range(rows):
        line = "  ".join(cells[r][c].rjust(widths[c]) for c in range(cols))
        lines.append(f"[ {line} ]")
    return "\n".join(lines)
