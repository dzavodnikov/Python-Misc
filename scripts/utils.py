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


def permissions_to_str(octal: str) -> str:
    bin_lst = [int(b) for b in list(f"{int(octal, 8):012b}")]
    char_lst = []

    # Set standard.
    standard = ("r", "w", "x")
    for idx in range(3, 12):
        char_lst += standard[idx % 3] if bin_lst[idx] else "-"

    # Set special.
    special = ("s", "s", "t")
    for idx in range(3):
        if bin_lst[idx]:
            char_lst[3 * idx + 2] = special[idx]

    return "".join(char_lst)


def permissions_to_oct(string: str) -> str:
    string = string.replace("_", "")
    if len(string) != 9:
        raise RuntimeError(f"Permission string '{string}' is not correct. Use format 'rwx---r-x' or 'rwx_---_r-x'")

    char_lst = list(string)
    bin_lst = []

    # Set special.
    for idx in range(2, 9, 3):
        bin_lst += "1" if char_lst[idx] in "st" else "0"

    # Set standard.
    for idx in range(9):
        bin_lst += "1" if char_lst[idx] in "rwxst" else "0"

    bin_groups = [bin_lst[idx : idx + 3] for idx in range(0, 12, 3)]
    oct_groups = [int("".join(g), 2) for g in bin_groups]
    oct_str = "".join([str(og) for og in oct_groups])
    return str(int(oct_str))  # Reduce decimal number.


# See:
#   https://chmod-calculator.com/
#   https://www.linkedin.com/pulse/understanding-special-permissions-linux-sticky-bit-setgid-ravi-pandey-rhvpf/
class TestPermissions(unittest.TestCase):

    def test_simple_oct_to_str(self):
        self.assertEqual(permissions_to_str("0"), "---------")
        self.assertEqual(permissions_to_str("700"), "rwx------")
        self.assertEqual(permissions_to_str("755"), "rwxr-xr-x")
        self.assertEqual(permissions_to_str("777"), "rwxrwxrwx")

    def test_simple_str_to_oct(self):
        self.assertEqual(permissions_to_oct("---------"), "0")
        self.assertEqual(permissions_to_oct("rwx------"), "700")
        self.assertEqual(permissions_to_oct("rwxr-xr-x"), "755")
        self.assertEqual(permissions_to_oct("rwxrwxrwx"), "777")
        self.assertEqual(permissions_to_oct("rwx_rwx_rwx"), "777")

    def test_special_oct_to_str(self):
        self.assertEqual(permissions_to_str("1755"), "rwxr-xr-t")
        self.assertEqual(permissions_to_str("2755"), "rwxr-sr-x")
        self.assertEqual(permissions_to_str("4755"), "rwsr-xr-x")
        self.assertEqual(permissions_to_str("7777"), "rwsrwsrwt")

    def test_special_str_to_oct(self):
        self.assertEqual(permissions_to_oct("rwxr-xr-t"), "1755")
        self.assertEqual(permissions_to_oct("rwxr-sr-x"), "2755")
        self.assertEqual(permissions_to_oct("rwsr-xr-x"), "4755")
        self.assertEqual(permissions_to_oct("rwsrwsrwt"), "7777")


if __name__ == "__main__":
    unittest.main()
