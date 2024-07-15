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


if __name__ == "__main__":
    print(sizeof_fmt(10))
    print(sizeof_fmt(5 * 1024 + 200))

    print(permissions_str(777))
    print(permissions_oct("rwxr-xr-x"))
