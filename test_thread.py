import threading

from logkk import LogManager, Level
from logkk.handler import FileHandler

fmt = "[{datetime}] [{level}] [{name}] {message}"
handler = FileHandler(filepath="demo.log")
log_manager = LogManager(level=Level.INFO, fmt=fmt, handlers=[handler])
logger = log_manager.get_logger(name="hello")


def print_log(idx):
    for _ in range(20000):
        logger.info(f"this is log by node0{idx}: "
                    f"Though the earlier answers are correct, there's a small complication it would help to remark on")


if __name__ == "__main__":
    tasks = []
    for i in range(1, 5):
        t = threading.Thread(target=print_log, args=(i, ))
        t.start()
        tasks.append(t)

    for task in tasks:
        task.join()

"""
结论：测试后发现，多线程情况下，FileHandler必须使用锁才能保证安全，不使用锁会导致日志打印不全
"""
