from hw_3.easy import Matrix
import numpy as np


class HashMixin:
    def __hash__(self) -> int:
        """
        Можем считать как сумму элементов данного массива,
        тогда достаточно просто найти коллизию для данной функции хеширования
        :return:
        """
        return int(sum(map(sum, self.matrix)))


class HashMatrix(Matrix, HashMixin):
    cache = {}

    def __matmul__(self, other):
        res = (hash(self), hash(other))
        if res not in self.cache:
            self.cache[res] = super().__matmul__(other)
        else:
            print("SKIP: use cache")
        return HashMatrix(self.cache[res].matrix)


if __name__ == "__main__":
    np.random.seed(0)
    matrix_a = HashMatrix(np.array([[1, 0], [1, 0]]))
    matrix_c = HashMatrix(np.array([[0, 2], [0, 0]]))
    assert hash(matrix_a) == hash(matrix_c)
    matrix_b = matrix_d = HashMatrix(np.array([[1, 0], [0, 1]]))

    HashMatrix.write_to_file(matrix_a, "artifacts/hard/A.txt")
    HashMatrix.write_to_file(matrix_b, "artifacts/hard/B.txt")
    HashMatrix.write_to_file(matrix_c, "artifacts/hard/C.txt")
    HashMatrix.write_to_file(matrix_d, "artifacts/hard/D.txt")

    HashMatrix.write_to_file(matrix_a @ matrix_b, "artifacts/hard/AB.txt")
    # наступает коллизия, если не очистить кеш
    # если не очистить, то получим просто результат AB
    HashMatrix.cache.clear()
    HashMatrix.write_to_file(matrix_c @ matrix_d, "artifacts/hard/CD.txt")

    print("Хеш матриц AB и CD")
    with open("artifacts/hard/hash.txt", "w") as f:
        f.write(f"Хеш функций:\n AB: {hash(matrix_a @ matrix_b)}\n CD: {hash(matrix_c @ matrix_d)}")
