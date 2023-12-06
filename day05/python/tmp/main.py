#!/usr/bin/env python3

import helper

LINES = """
50 98 2
52 50 48
0 15 37
37 52 2
39 0 15
49 53 8
0 11 42
42 0 7
57 7 4
88 18 7
18 25 70
45 77 23
81 45 19
68 64 13
0 69 1
1 0 69
60 56 37
56 93 4
""".strip().splitlines()


def make_list(x: int, y: int) -> list[int]:
    return [x, x + y - 1]


def process(line: str) -> None:
    a, b, c = [int(n) for n in line.split()]
    list_a = make_list(a, c)
    list_b = make_list(b, c)
    print(f"{list_a}    {list_b}")


def main():
    # for line in LINES:
    # process(line)
    li = [1, 2, 3, 4]
    result = [list(t) for t in helper.grouper(li, 2)]
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
