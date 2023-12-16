#!/usr/bin/env python3

import helper


def hash_it(s: str) -> int:
    total = 0

    for c in s:
        total += ord(c)
        total *= 17
        total %= 256

    return total


def main() -> None:
    # fname = "example.txt"
    fname = "input.txt"

    line = helper.read(fname).strip()
    parts = line.split(",")

    total = 0
    for part in parts:
        value = hash_it(part)
        total += value
        # print(f"{part}: {value}")
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
