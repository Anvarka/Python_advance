import numpy as np


def checker_matmul(matrix1, matrix2):
    rows1 = len(matrix1)
    cols2 = len(matrix2[0])
    assert rows1 == cols2


def checker_mul_add(matrix1, matrix2):
    rows1 = len(matrix1)
    cols1 = len(matrix1[0])
    rows2 = len(matrix2)
    cols2 = len(matrix2[0])
    assert rows1 == rows2 and cols1 == cols2


class Matrix:
    def __init__(self, matrix):
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.matrix = matrix

    def __add__(self, other_matrix):
        checker_mul_add(self.matrix, other_matrix.matrix)

        return Matrix([[x1 + x2 for x1, x2 in zip(row1, row2)] for row1, row2 in zip(self.matrix, other_matrix.matrix)])

    def __str__(self) -> str:
        return '\n'.join(['   '.join(map(str, row)) for row in self.matrix])

    def __mul__(self, other_matrix):
        checker_mul_add(self.matrix, other_matrix.matrix)

        return Matrix([[x1 * x2 for x1, x2 in zip(row1, row2)] for row1, row2 in zip(self.matrix, other_matrix.matrix)])

    def __matmul__(self, other_matrix):
        checker_matmul(self.matrix, other_matrix.matrix)
        return Matrix(
            [[sum([self.matrix[i][k] * other_matrix.matrix[k][j] for k in range(len(other_matrix.matrix))]) for j in
              range(len(other_matrix.matrix[0]))] for i in range(len(other_matrix.matrix))])

    @staticmethod
    def write_to_file(res_matrix, fname):
        with open(fname, 'w') as file:
            file.write(str(res_matrix))


if __name__ == "__main__":
    np.random.seed(0)
    matrix1 = np.random.randint(0, 10, (10, 10))
    matrix2 = np.random.randint(0, 10, (10, 10))
    Matrix.write_to_file((Matrix(matrix1) + Matrix(matrix2)), "artifacts/easy/matrix+.txt")
    Matrix.write_to_file((Matrix(matrix1) * Matrix(matrix2)), "artifacts/easy/matrix*.txt")
    Matrix.write_to_file((Matrix(matrix1) @ Matrix(matrix2)), "artifacts/easy/matrix@.txt")
