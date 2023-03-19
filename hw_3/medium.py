import numpy as np


class FileWriterMixin:
    def write_file(self, fname):
        with open(fname, 'w') as f:
            f.write(str(self))


class StrBeautyPresentMixin:
    def __str__(self):
        return '\n'.join(['\t'.join(map(str, row)) for row in self.matrix])


class GetterSetterMixin:
    def __init__(self, matrix):
        self.matrix = matrix

    @property
    def matrix(self):
        print("getter")
        return self._matrix

    @matrix.setter
    def matrix(self, new_data):
        print("setter")
        self._matrix = new_data


class MediumMatrix(np.lib.mixins.NDArrayOperatorsMixin, FileWriterMixin, StrBeautyPresentMixin, GetterSetterMixin):

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = tuple(x.matrix if isinstance(x, MediumMatrix) else x for x in inputs)

        result = getattr(ufunc, method)(*inputs, **kwargs)
        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.matrix)


if __name__ == "__main__":
    np.random.seed(0)
    matrix1 = np.random.randint(0, 10, (10, 10))
    matrix2 = np.random.randint(0, 10, (10, 10))
    a = MediumMatrix(matrix1)
    b = MediumMatrix(matrix2)
    (a + b).write_file("artifacts/medium/matrix+.txt")
    (a * b).write_file("artifacts/medium/matrix*.txt")
    (a @ b).write_file("artifacts/medium/matrix@.txt")
