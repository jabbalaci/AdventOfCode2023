#!/usr/bin/env python3

import math
from itertools import cycle
from pprint import pprint

import helper


class Network:
    def __init__(self, lines: list[str]) -> None:
        self.parse(lines)
        self.starting_points: list[str] = self.collect_starting_points()

    def collect_starting_points(self) -> list[str]:
        return [k for k in self.d if k.endswith("A")]

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

    def can_stop(self, node: str) -> bool:
        return node.endswith("Z")

    def process(self, label: str) -> int:
        t = self.d[label]
        counter = 0
        #
        for c in cycle(self.steps):
            which = 0  # left
            if c == "R":
                which = 1  # right
            #
            node = t[which]
            counter += 1
            if self.can_stop(node):
                break
            #
            t = self.d[node]
        #
        return counter

    def start(self) -> None:
        collect = []
        for node in self.starting_points:
            collect.append(self.process(node))
        #
        # print(collect)
        result = math.lcm(*collect)  # least common multiple
        print(result)

    def debug(self) -> None:
        print(self.steps)
        pprint(self.d)


def main() -> None:
    # lines = helper.read_lines("example1.txt")
    # lines = helper.read_lines("example2.txt")
    # lines = helper.read_lines("example3.txt")
    lines = helper.read_lines("input.txt")

    n = Network(lines)

    n.start()

    # n.debug()


##############################################################################

if __name__ == "__main__":
    main()
