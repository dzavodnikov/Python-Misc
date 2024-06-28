#!/usr/bin/env python

import time
from http.client import RemoteDisconnected
from typing import Callable
from urllib.error import URLError
from urllib.request import urlopen


def sizeof_fmt(size: int) -> str:
    fmt = lambda s, u: f"{s:.1f} {u}"

    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if abs(size) < 1024:
            return fmt(size, unit)
        size = int(size / 1024)

    return fmt(size, "PiB")


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


@repeat_if(RemoteDisconnected, URLError)
def check_if_url_available(url: str, timeout: int = 15) -> None:
    with urlopen(url, timeout=timeout) as resp:
        code = resp.getcode()
        if code not in [200, 302]:
            raise URLError(reason=f"URL '{url}' return status {code}")


if __name__ == "__main__":
    check_if_url_available("http://localhost:9090")
