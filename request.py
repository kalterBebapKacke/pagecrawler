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
            return  ans
        if generator:
            headers = gen.__next__()
            if headers == 0:
                break
    return selenium_requests()


def selenium_requests(url:str, keyword:str):
    return NotImplemented

url = "https://lichess.org/"
print(request(url, "lichess"))