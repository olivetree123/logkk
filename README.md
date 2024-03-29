# Logkk

**易于使用**且**线程安全**的日志模块

### 安装
```shell
pip install logkk
```

### 基础使用：
```python
from logkk import LogManager

log_manager = LogManager()
log_manager.info("this is a info log")
log_manager.warn("this is a warn log")

logger = log_manager.get_logger(name="hello")
logger.info("this is a info log")
logger.warn("this is a warn log")
```

### 使用文件记录日志：

```python
from logkk import LogManager, Level
from logkk.handlers import FileHandler

fmt = "[{datetime}] [{level}] [{name}] {message}"
handler = FileHandler(filepath="/var/log/demo.log")
log_manager = LogManager(level=Level.INFO, fmt=fmt, handlers=[handler])
logger = log_manager.get_logger(name="hello")
logger.info("this is a info log")
logger.warn("this is a warn log")
```

### 作为函数装饰器使用
给每个函数添加装饰器，打印函数的参数和返回值，在程序调试阶段是非常好用的。
```python
def log_required(f):

    def func(f2):

        @wraps(f2)
        def decorated(request, *args, **kwargs):
            name = f"{f.__module__}:{f.__name__}"
            logger = log.get_logger(name=name)
            logger.info(f"{request.method} {request.path}")
            logger.info("params=", request.body)
            setattr(request, "logger", logger)
            r = f(request, *args, **kwargs)
            if isinstance(r, BaseResponse):
                logger.info("response=", r.result)
            else:
                logger.info("response=", r)
            return r

        return decorated

    return func(f)


@log_required
def UpdateMyInfoHandler(request: HttpRequest):
    # ...
    return {"code": 0, "message":"OK"}
```

### 技术方案说明
写日志文件主要有两种方式：
1. 每次写日志时打开文件，写完后关闭文件；
2. 保持一个文件句柄，每次写日志时直接写入文件；

很明显，第二种方式效率更高，但是一直保持一个打开的文件对象，会不会有问题呢？  
查询了一些资料后发现，并没有什么问题，因为：
> 当进程退出时，不管是正常退出还是异常退出，亦或是进程被强制杀掉，操作系统都会回收给进程分配的资源，
也就是说系统会关闭这个文件句柄。

当进程异常退出时，为了保证我们写的日志不丢失，每次写日志时需要调用flush将日志落盘。因为write只是将内容写到系统缓冲区，并没有写到磁盘上，
当进程异常退出时，系统缓冲区的数据会丢失，而flush就是将系统缓冲区的内容写到磁盘上，并清空系统缓冲区。

另外，如果多线程写日志，会出现写入混乱的情况，所以需要加锁，虽然这样会影响效率，但是更加安全可靠。