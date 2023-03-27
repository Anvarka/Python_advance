from threading import Thread
from multiprocessing import Process

from hw_1.figureasttree4.fibonacci import fib
from timeit import timeit


def threading(n):
    threads = []
    for _ in range(10):
        thread = Thread(target=fib, args=(n,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def processing(n):
    processes = []
    for _ in range(10):
        process = Process(target=fib, args=(n,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


def usual(n):
    for _ in range(10):
        fib(n)


if __name__ == "__main__":
    n = 100_000
    with open("artifacts/easy/time.txt", "w") as f:
        f.write(f"Syncronous: {timeit('usual(n)', number=10, globals=globals()) / 10 * 1000} ms\n")
        f.write(f"Threading: {timeit('threading(n)', number=10, globals=globals()) / 10 * 1000} ms\n")
        f.write(f"Process: {timeit('processing(n)', number=10, globals=globals()) / 10 * 1000} ms\n")
