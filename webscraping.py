import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from types import MappingProxyType
import requests
import multiprocessing as mp
from bs4 import BeautifulSoup
from selenium_stealth import stealth
import time

if __name__ == '__main__':
    import headers
else:
    from . import headers
import sys

sys.setrecursionlimit(10000)

basic_request_header = dict(
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Opera GX";v="106"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest ': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0'
    }
)

request_info = tuple[str, str, dict]


def headers_generator():
    for x in headers.list_headers.values():
        yield x
    yield 0


def _request(url: str, keyword: str, headers: dict = None):
    if headers is None:
        headers = {}
    ans = requests.request("get", url=url, headers=headers).text
    if ans.__contains__(keyword):
        return ans
    else:
        return selenium_requests(url, keyword)


def selenium_requests(url: str, keyword: str):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(url)
    waiting = 0
    while True:
        time.sleep(waiting)
        source = driver.page_source
        print(waiting)
        if source.__contains__(keyword):
            driver.quit()
            return BeautifulSoup(source, 'html.parser')
        if waiting == 40:
            break
        waiting += 1
    driver.quit()




def func_request(webscraping_class, args):
    return webscraping_class._request(*args)


def setup(self):
    if os.environ['chromedriver_update'] == 'False':
        # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        os.environ['chromedriver_update'] = 'True'

    def request(self, request_info_: list[request_info], process: int = 1):
        for i, single_info in enumerate(request_info_):
            new_list = [self]
            new_list.append(single_info)
            request_info_[i] = new_list
        print(request_info_)
        print(len(request_info_[0]))
        res = self._run(process=process, func=func_request, args=request_info_)
        print(res)


    def get_in_string(self, string: str, Str1, Str2):
        if string.find(Str1) != -1:
            string = string[string.find(Str1) + len(Str1):]
            string = string[:string.find(Str2)]
            return string
        else:
            return False


def test(arg):
    time.sleep(3)
    return arg


if __name__ == '__main__':
    a: request_info = ('https://www.ecosia.org/?c=de', '', basic_request_header)
    print(c.request([a, a]))
