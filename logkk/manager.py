from logkk.level import Level
from logkk.logger import Logger
from logkk.handlers import Handler

DEFAULT_FORMAT = "[{datetime}] [{level}] [{module_name}] [{function_name}] {message}"


class LogManager(object):

    def __init__(self,
                 name="logkk",
                 level=Level.INFO,
                 fmt=DEFAULT_FORMAT,
                 handlers=None):
        self.name = name
        self.level = level
        self.fmt = fmt
        self.handlers = handlers or []
        self._default_logger = self.get_logger(self.name)

    def set_format(self, fmt: str):
        self.fmt = fmt

    def set_level(self, level: int):
        self.level = level

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)

    def get_logger(self, module_name=None, function_name=None) -> Logger:
        """
        :param module_name: 模块名称或者文件名称
        :param function_name: 函数名称
        :return: Logger对象
        """
        return Logger(module_name=module_name or self.name,
                      function_name=function_name,
                      level=self.level,
                      fmt=self.fmt,
                      handlers=self.handlers)

    def debug(self, *args, **kwargs):
        self._default_logger.info(*args, **kwargs)

    def info(self, *args, **kwargs):
        self._default_logger.info(*args, **kwargs)

    def warn(self, *args, **kwargs):
        self._default_logger.info(*args, **kwargs)

    def error(self, *args, **kwargs):
        self._default_logger.info(*args, **kwargs)


if __name__ == "__main__":
    log_manager = LogManager()
    log_manager.info("this is a info log")
    log_manager.warn("this is a warn log")
    logger = log_manager.get_logger(module_name="main")
    logger.info("this is a info log")
    logger.warn("this is a warn log")
