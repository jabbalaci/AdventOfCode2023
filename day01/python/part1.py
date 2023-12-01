#!/usr/bin/env python3

import helper


def main() -> None:
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    total = 0
    for line in lines:
        first, last = -1, -1
        for c in line:
            if c.isdigit():
                first = int(c)
                break
            #
        #
        for c in line[::-1]:
            if c.isdigit():
                last = int(c)
                break
            #
        #
        total += first * 10 + last
    #
    print(total)


##############################################################################

if __name__ == "__main__":
    main()
