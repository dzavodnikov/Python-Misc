#!/usr/bin/env python


def sizeof_fmt(size_bytes: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    fmt = lambda s, u: f"{s:.1f} {u}" if units.index(u) > 0 else f"{s:.0f} {u}"

    s: float = size_bytes
    for u in units:
        if abs(s) < 1024.0:
            return fmt(s, u)
        s = s / 1024.0

    return fmt(s, "PiB")


if __name__ == "__main__":
    print(sizeof_fmt(10))
    print(sizeof_fmt(5 * 1024 + 200))
