import requests
from types import MappingProxyType
import headers

def headers_generator():
    for x in headers.list_headers.values():
        yield x
    yield 0

def request(url:str, keyword:str, headers:MappingProxyType=MappingProxyType({})):
    generator = False
    gen = None
    if headers == MappingProxyType({}):
        generator = True
        gen = headers_generator()
        headers = gen.__next__()
    while True:
        ans = requests.request("get", url=url, headers=headers).text
        if ans.__contains__(keyword):
            break
        if generator:
            headers = gen.__next__()


def selenium_requests():
    pass
