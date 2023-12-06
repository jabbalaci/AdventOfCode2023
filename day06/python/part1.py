#!/usr/bin/env python3

import math
from typing import Iterable

import helper


def parse(lines: list[str]) -> Iterable[tuple[int, int]]:
    def parse_line(line: str) -> list[int]:
        right = line.split(":")[1]
        return [int(n) for n in right.split()]

    numbers1 = parse_line(lines[0])
    numbers2 = parse_line(lines[1])

    return zip(numbers1, numbers2)


def process(pair: tuple[int, int]) -> int:
    time, dist = pair

    total = 0
    for msec in range(1, time):  # discard first and last
        speed = msec
        remaining = time - msec
        distance_done = speed * remaining
        if distance_done > dist:
            total += 1
        #
    #
    return total


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    pairs = parse(lines)
    numbers = []
    for pair in pairs:
        numbers.append(process(pair))
    #
    result = math.prod(numbers)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
