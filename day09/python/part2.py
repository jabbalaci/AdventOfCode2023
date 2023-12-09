#!/usr/bin/env python3

import helper


def all_zero(li: list[int]) -> bool:
    for e in li:
        if e != 0:
            return False
        #
    #
    return True


def process(numbers: list[int]) -> int:
    data: list[list[int]] = [numbers]

    curr: list[int] = data[-1]
    while not all_zero(curr):
        new: list[int] = []
        for i in range(1, len(curr)):
            new.append(curr[i] - curr[i - 1])
        #
        data.append(new)
        curr = new
    #
    data.reverse()
    for i in range(1, len(data)):
        prev = data[i - 1]
        curr = data[i]
        add = curr[-1] + prev[-1]
        curr.append(add)
    #
    # print(data)
    result = data[-1][-1]

    # print(numbers)
    # print(result)
    # print("---")

    return result


def main() -> None:
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    total = 0
    for line in lines:
        numbers = [int(n) for n in line.split()]
        numbers.reverse()  # This! :)
        total += process(numbers)
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
