#!/usr/bin/env python

import time
from http.client import RemoteDisconnected
from typing import Callable
from urllib.error import URLError
from urllib.request import urlopen


def sizeof_fmt(size_bytes: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    fmt = lambda s, u: f"{s:.1f} {u}" if units.index(u) > 0 else f"{s:.0f} {u}"

    s: float = size_bytes
    for u in units:
        if abs(s) < 1024.0:
            return fmt(s, u)
        s = s / 1024.0

    return fmt(s, "PiB")


def permissions_str(octal: int) -> str:
    permission = ("---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx")

    result = []
    octal_str = f"{octal:04d}"
    for v in [int(n) for n in octal_str]:
        result += permission[v]
    return "".join(result)


def permissions_oct(string: str) -> int:
    permission = ("---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx")

    result = ""
    for v in [string[x : x + 3] for x in range(0, len(string), 3)]:
        result += str(permission.index(v))
    return int(result)


def repeat_if(
    *exceptions: type[Exception],
    max_request_repeat: int = 30,
    repeat_sleep_sec: int = 10,
    print_info: bool = True,
):
    def repeat_if_wrapper(func: Callable):
        def wrapper(*args, **kwargs):
            args_str = ",".join([f"{str(val)}" for val in args])
            kwargs_str = ",".join([f"{key}={val}" for key, val in kwargs.items()])
            fn_str = f'#{func.__name__}({",".join([val for val in [args_str, kwargs_str] if val])})'

            happens = set()
            for rep in range(max_request_repeat):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    step = rep + 1

                    happens.add(str(e))

                    if print_info:
                        repeat = f"{step}/{max_request_repeat}"
                        print(f"Waiting {repeat_sleep_sec} sec and repeat {repeat} for {fn_str}: {str(e)}")

                    time.sleep(repeat_sleep_sec)
            raise Exception(f'Fail with {fn_str}: {",".join(happens)}')

        return wrapper

    return repeat_if_wrapper


@repeat_if(RemoteDisconnected, URLError, max_request_repeat=3, repeat_sleep_sec=1)
def check_if_url_available(url: str, timeout: int = 1) -> None:
    with urlopen(url, timeout=timeout) as resp:
        code = resp.getcode()
        if code not in [200, 302]:
            raise URLError(reason=f"URL '{url}' return status {code}")


if __name__ == "__main__":
    print(sizeof_fmt(10))
    print(sizeof_fmt(5 * 1024 + 200))

    print(permissions_str(777))
    print(permissions_oct("rwxr-xr-x"))

    check_if_url_available("http://localhost:9090")
