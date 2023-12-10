#!/usr/bin/env python3

import helper

cfg = {"red": 12, "green": 13, "blue": 14}


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


def analyze(line: str) -> tuple[int, bool]:
    left, right = line.split(":")
    _id = int(left.split()[-1])
    sets: list[dict] = get_sets(right)

    ok = True  # the whole game
    for d in sets:
        good = True  # current set of cubes
        for k, v in d.items():
            if v > cfg[k]:
                good = False
            #
        #
        if not good:
            ok = False
        #
    #
    return _id, ok


def main() -> None:
    # lines = helper.read_lines("example.txt")  # OK: 1, 2 and 5
    lines = helper.read_lines("input.txt")

    total = 0
    for line in lines:
        _id, ok = analyze(line)
        if ok:
            total += _id
        #
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
