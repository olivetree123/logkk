import random
import multiprocessing

from logkk import LogManager, Level
from logkk.handler import FileHandler

fmt = "[{datetime}] [{level}] [{name}] {message}"
handler = FileHandler(filepath="demo.log")
log_manager = LogManager(level=Level.INFO, fmt=fmt, handlers=[handler])
logger = log_manager.get_logger(name="hello")


def print_log():
    idx = random.randint(1, 10)
    for _ in range(20000):
        logger.info(f"this is log by node0{idx}: Though the earlier answers are correct, there's a small complication it would help to remark on")


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)
    pool.apply(print_log)
    pool.apply(print_log)
    pool.apply(print_log)
    pool.apply(print_log)
    pool.close()
    pool.join()
    # print("outputs=", outputs)

