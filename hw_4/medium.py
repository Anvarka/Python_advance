import math
import logging
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import cpu_count
from timeit import timeit


logging.basicConfig(filename="artifacts/medium/log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
general_logger = logging.getLogger("general_logger")


def integrate_part(kwargs):
    def integrate(f, a, b, n_jobs=1, job=0, n_iter=1000):
        acc = 0
        step = (b - a) / n_iter

        job_start_pos = (b - a) / n_jobs
        a += job_start_pos * job
        b = a + job_start_pos
        general_logger.debug(f"{job} integrates from {a} to {b}")
        n_iter //= n_jobs
        for i in range(n_iter):
            acc += f(a + i * step) * step
        return acc
    return integrate(**kwargs)


def integrate_with_process_pool(f, a, b, n_jobs=1, n_iter=1000):
    with ProcessPoolExecutor(n_jobs) as executor:
        general_logger.debug(f"ProcessPoolExecutor with {n_jobs} started to work")
        args = [{"f": f, "a": a, "b": b, "n_jobs": n_jobs, "n_iter": n_iter, "job": i} for i in range(n_jobs)]
        return sum(executor.map(integrate_part, args))


def integrate_with_thread_pool(f, a, b, n_jobs=1, n_iter=1000):
    with ThreadPoolExecutor(n_jobs) as executor:
        general_logger.debug(f"ThreadPoolExecutor with {n_jobs} started to work")
        args = [{"f": f, "a": a, "b": b, "n_jobs": n_jobs, "n_iter": n_iter, "job": i} for i in range(n_jobs)]
        return sum(executor.map(integrate_part, args))


if __name__ == "__main__":
    cpu_count = cpu_count()
    with open("artifacts/medium/time.txt", "w") as f:
        general_logger.debug("THREAD START")
        f.write(f"thread\n")
        for count_job in range(1, 2 * cpu_count + 1):
            f.write(f"job_count {count_job}: {timeit(lambda: integrate_with_thread_pool(math.cos, 0, math.pi / 2, n_jobs=count_job), number=10) / 10 * 1000} ms\n")
        general_logger.debug("THREAD END")

        general_logger.debug("PROCESSING START")
        f.write(f"process:\n")
        for i in range(1, 2 * cpu_count + 1):
            f.write(f"job_count {i}: {timeit(lambda: integrate_with_process_pool(math.cos, 0, math.pi / 2, n_jobs=i), number=10) / 10 * 1000} ms\n")
        general_logger.debug("PROCESSING END")

