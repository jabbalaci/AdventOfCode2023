#!/usr/bin/env python3

import helper


def process(line: str) -> int:
    numbers = line.split(":")[1]
    left, right = numbers.split(" | ")
    # print(left, "|", right)
    left_numbers = [int(n) for n in left.split()]
    right_numbers = [int(n) for n in right.split()]

    # make sure left and right group has no duplicates
    assert len(left_numbers) == len(set(left_numbers))
    assert len(right_numbers) == len(set(right_numbers))

    a = set(left_numbers)
    b = set(right_numbers)
    common = a.intersection(b)

    result = 0
    if common:
        size = len(common)
        result = 2 ** (size - 1)
    #
    return result


def main() -> None:
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    total = 0
    for line in lines:
        total += process(line)
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
