import requests
import threading
from abc import ABC

from .errors import HttpHandlerError

file_lock = threading.Lock()
stream_lock = threading.Lock()


class Handler(ABC):

    def write(self, content):
        pass


class StreamHandler(Handler):

    def write(self, content):
        with stream_lock:
            print(content)


class FileHandler(Handler):

    def __init__(self, filepath, encoding="utf8"):
        self.filepath = filepath
        self.encoding = encoding
        self.file_obj = None

    def write(self, content):
        with file_lock:
            if not self.file_obj:
                self.file_obj = open(file=self.filepath,
                                     mode="a+",
                                     encoding=self.encoding)
            self.file_obj.write(content + "\n")

    def close(self):
        self.file_obj.close()


import aiohttp


class HttpHandler(Handler):

    def __init__(self, url):
        self.url = url
        self.client = aiohttp.ClientSession()

    def write(self, content):
        # TODO: 如何做到异步发送
        params = {"log": content}
        self.client.post(self.url, json=params)
        # r = requests.post(self.url, params)
        # if not r.ok:
        #     raise HttpHandlerError(r)
