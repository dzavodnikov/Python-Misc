#!/usr/bin/env python


def sizeof_fmt(size: int) -> str:
    fmt = lambda s, u: f"{s:.1f} {u}"

    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if abs(size) < 1024.0:
            return fmt(size, unit)
        size = int(size / 1024.0)

    return fmt(size, "PiB")
