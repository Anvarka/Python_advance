from multiprocessing import Process, Queue, Pipe
import logging
import time
import codecs

# можно через очередь Queue поддерживать связь между двумя процессами
# https://superfastpython.com/multiprocessing-queue-in-python/
# можно через connections, то есть через Pipe поддерживать
# https://superfastpython.com/multiprocessing-pipe-in-python/
# main -(queue)-> a -(conn)-> b -(queue)-> main

logging.basicConfig(filename="artifacts/hard/log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger_info = logging.getLogger("logger")


def a_process(queue_from_main, conn_to_b):
    while True:
        msg = queue_from_main.get()
        if msg is None:
            logger_info.debug(f'killed process A')
            conn_to_b.send(None)
            break
        logger_info.debug(f'A process: get "{msg}" from main process')
        msg = msg.lower()
        conn_to_b.send(msg)
        logger_info.debug(f'A process: send "{msg}" to process B')
        time.sleep(5)


def b_process(conn_from_a, queue_to_main):
    while True:
        msg = conn_from_a.recv()
        if msg is None:
            logger_info.debug(f'killed process B')
            break
        logger_info.debug(f'B process: get "{msg}" from process A')
        msg = codecs.encode(msg, 'rot_13')
        queue_to_main.put(msg)
        logger_info.debug(f'B process: send "{msg}" to main process')


if __name__ == "__main__":
    stdin_queue = Queue()
    stdout_queue = Queue()
    conn_receive, conn_sender = Pipe()

    a = Process(target=a_process, args=(stdin_queue, conn_sender))
    b = Process(target=b_process, args=(conn_receive, stdout_queue))

    a.start()
    b.start()

    while True:
        text = input()
        if text == "":
            stdin_queue.put(None)
            logger_info.debug("Main process: kill all process")
            break

        stdin_queue.put(text)
        logger_info.debug(f'Main process: send "{text}" to process A')
        encryption_text = stdout_queue.get()
        logger_info.debug(f'Main process: get "{text}" from process B')
        print(encryption_text)

    a.join()
    b.join()

