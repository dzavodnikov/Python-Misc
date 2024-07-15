#!/usr/bin/env python

import unittest


def sizeof_fmt(size_bytes: int) -> str:
    units = ("B  ", "KiB", "MiB", "GiB", "TiB")
    fmt = lambda s, u: f"{s:.1f} {u}" if units.index(u) > 0 else f"{s:.0f} {u}"

    s: float = size_bytes
    for u in units:
        if abs(s) < 1024.0:
            return fmt(s, u)
        s = s / 1024.0

    return fmt(s, "PiB")


class TestSizeOfFmt(unittest.TestCase):

    def test_size_of_fmt(self):
        self.assertEqual("10 B  ", sizeof_fmt(10))
        self.assertEqual("5.2 KiB", sizeof_fmt(5 * 1024 + 200))


if __name__ == "__main__":
    unittest.main()
