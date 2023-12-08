#!/usr/bin/env python3

# first approach
# impossibly slow

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

    def can_stop(self, nodes: list[str]) -> bool:
        return all([node.endswith("Z") for node in nodes])

    def start(self) -> None:
        d = self.d
        now = self.starting_points
        counter = 0
        #
        for c in cycle(self.steps):
            which = 0  # left
            if c == "R":
                which = 1  # right
            #
            nodes = [d[pos][which] for pos in now]
            counter += 1
            if self.can_stop(nodes):
                break
            #
            now = nodes
        #
        print(counter)

    def debug(self) -> None:
        print(self.steps)
        pprint(self.d)
        print(self.starting_points)


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
