#!/usr/bin/env python3

from itertools import cycle
from pprint import pprint

import helper


class Network:
    def __init__(self, lines: list[str]) -> None:
        self.parse(lines)

    def parse(self, lines: list[str]) -> None:
        self.steps = lines[0]
        d: dict[str, tuple[str, str]] = {}
        for line in lines[2:]:
            key, right = line.split(" = ")
            right = right.lstrip("(").rstrip(")")
            value = tuple(right.split(", "))
            d[key] = value  # type: ignore
        #
        self.d = d

    def start(self) -> None:
        t = self.d["AAA"]
        counter = 0
        #
        for c in cycle(self.steps):
            which = 0  # left
            if c == "R":
                which = 1  # right
            #
            node = t[which]
            counter += 1
            if node == "ZZZ":
                break
            #
            t = self.d[node]
        #
        print(counter)

    def debug(self) -> None:
        print(self.steps)
        pprint(self.d)


def main() -> None:
    # lines = helper.read_lines("example1.txt")
    # lines = helper.read_lines("example2.txt")
    lines = helper.read_lines("input.txt")

    n = Network(lines)

    n.start()

    # n.debug()


##############################################################################

if __name__ == "__main__":
    main()
