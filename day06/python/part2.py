#!/usr/bin/env python3

import helper


def parse(lines: list[str]) -> tuple[int, int]:
    def parse_line(line: str) -> int:
        right = line.split(":")[1]
        return int(right.replace(" ", ""))

    number1 = parse_line(lines[0])
    number2 = parse_line(lines[1])

    return (number1, number2)


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

    pair = parse(lines)
    result = process(pair)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
