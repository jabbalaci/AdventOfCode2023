#!/usr/bin/env python3

import math

import helper


def get_sets(right: str) -> list[dict]:
    result: list[dict] = []
    sets = right.split(";")
    for _set in sets:
        d = {}
        parts = _set.split(",")
        for part in parts:
            part = part.strip()
            amount, color = part.split()
            d[color] = int(amount)
        #
        result.append(d)
    #
    return result


def analyze(line: str) -> dict:
    _, right = line.split(":")
    sets: list[dict] = get_sets(right)

    d = {"red": 0, "green": 0, "blue": 0}
    for _set in sets:
        for k, v in _set.items():
            if v > d[k]:
                d[k] = v
            #
        #
    #
    return d


def main() -> None:
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    total = 0
    for line in lines:
        d: dict = analyze(line)
        total += math.prod(d.values())
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
