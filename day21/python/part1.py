#!/usr/bin/env python3

import sys
from typing import NamedTuple

import helper

# ----------------------------------------------------------------------------


class Point(NamedTuple):
    row: int
    col: int


# ----------------------------------------------------------------------------


class Garden:
    def __init__(self, fname: str) -> None:
        self.lines = helper.read_lines(fname)
        self.no_of_rows = len(self.lines)
        self.no_of_cols = len(self.lines[0])
        self.start_point = self.find_start_point()
        self.positions: set[Point] = set([self.start_point])

    def find_start_point(self) -> Point:
        for i, line in enumerate(self.lines):
            for j, c in enumerate(line):
                if c == "S":
                    return Point(row=i, col=j)
                #
            #
        #
        assert False, "We should never get here"

    def can_go_up(self, p: Point) -> bool:
        return (p.row > 0) and (self.lines[p.row - 1][p.col] != "#")

    def can_go_down(self, p: Point) -> bool:
        return (p.row < self.no_of_rows - 1) and (self.lines[p.row + 1][p.col] != "#")

    def can_go_left(self, p: Point) -> bool:
        return (p.col > 0) and (self.lines[p.row][p.col - 1] != "#")

    def can_go_right(self, p: Point) -> bool:
        return (p.col < self.no_of_cols - 1) and (self.lines[p.row][p.col + 1] != "#")

    def get_possible_neighbors(self, p: Point) -> list[Point]:
        result: list[Point] = []

        if self.can_go_up(p):
            result.append(Point(row=p.row - 1, col=p.col))
        if self.can_go_down(p):
            result.append(Point(row=p.row + 1, col=p.col))
        if self.can_go_left(p):
            result.append(Point(row=p.row, col=p.col - 1))
        if self.can_go_right(p):
            result.append(Point(row=p.row, col=p.col + 1))
        #
        return result

    def move(self) -> None:
        new_positions: set[Point] = set()
        for p in self.positions:
            neighbors: list[Point] = self.get_possible_neighbors(p)
            for nb in neighbors:
                new_positions.add(nb)
            #
        #
        self.positions = new_positions

    def start(self) -> None:
        for step in range(64):
            self.move()
        #
        # self.show()
        result = len(self.positions)
        print(result)

    def show(self) -> None:
        for i, line in enumerate(self.lines):
            for j, c in enumerate(line):
                if Point(row=i, col=j) in self.positions:
                    sys.stdout.write("O")
                else:
                    sys.stdout.write(c)
                #
            #
            print()
        #

    def debug(self) -> None:
        print("# start point:", self.start_point)
        for line in self.lines:
            print(line)


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example.txt"
    fname = "input.txt"

    g = Garden(fname)

    g.start()

    # g.show()

    # g.debug()


##############################################################################

if __name__ == "__main__":
    main()
