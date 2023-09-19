from time import perf_counter
from functools import wraps

from loguru import logger

logger.add('log/debug.log', level='DEBUG',
           format='{time} {level} {message}', rotation='10 KB', compression='zip')

URL = 'https://www.olx.ua/uk/odessa/?search%5Bfilter_enum_state%5D%5B0%5D=new&search[private_business]=private'


HEADERS = {
    "Host": "www.olx.ua",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Connection": "keep-alive"
}


def timeit():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start = perf_counter()
            result = f(*args, **kwargs)
            print(f'Execution time: {round(perf_counter() - start, 2)}')
            return result
        return decorated_function
    return decorator
