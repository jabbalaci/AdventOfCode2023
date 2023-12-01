#!/usr/bin/env python3

import re

import helper

DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def text2number(text: str) -> int:
    if text.isdigit():
        return int(text)
    # else
    return DIGITS[text]


def process(line: str) -> int:
    m = re.search(r"1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine", line)
    assert m
    first = text2number(m.group())
    #
    m = re.search(r"1|2|3|4|5|6|7|8|9|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin", line[::-1])
    assert m
    last = text2number(m.group()[::-1])

    return first * 10 + last


def main() -> None:
    # lines = helper.read_lines("example2.txt")
    lines = helper.read_lines("input.txt")

    total = 0
    for line in lines:
        total += process(line)
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
