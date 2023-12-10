#!/usr/bin/env python3

from collections import deque
from enum import Enum, auto
from typing import NamedTuple

import helper

char = str


class Point(NamedTuple):
    row: int
    col: int


class Dir(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Grid:
    def __init__(self, fname: str, start_char: char) -> None:
        self.lines: list[str] = helper.read_lines(fname)
        self.start_char: char = start_char  # the real char under S (like "F" or "|", etc.)
        self.start_point: Point = self.find_start_point()
        self.no_of_rows = len(self.lines)
        self.no_of_cols = len(self.lines[0])

    def find_start_point(self) -> Point:
        for i, line in enumerate(self.lines):
            for j, c in enumerate(line):
                if c == "S":
                    return Point(row=i, col=j)
                #
            #
        #
        return Point(-1, -1)  # we should never get here

    def get_neighbors(self, curr: Point) -> list[Point]:
        result: list[Point] = []

        d: dict[char, tuple[Dir, Dir]] = {
            "F": (Dir.DOWN, Dir.RIGHT),
            "7": (Dir.LEFT, Dir.DOWN),
            "L": (Dir.UP, Dir.RIGHT),
            "J": (Dir.LEFT, Dir.UP),
            "-": (Dir.LEFT, Dir.RIGHT),
            "|": (Dir.UP, Dir.DOWN),
        }

        c: char = self.lines[curr.row][curr.col]
        # if it's the start point, replace "S" with the real char, like "F", "|", etc.
        if c == "S":
            c = self.start_char
        #
        for _dir in d.get(c, ()):
            i, j = curr.row, curr.col
            #
            if _dir == Dir.UP:
                i -= 1
            elif _dir == Dir.DOWN:
                i += 1
            elif _dir == Dir.LEFT:
                j -= 1
            elif _dir == Dir.RIGHT:
                j += 1
            else:
                assert False, "We should never get here"
            #
            # because -1 is the last element in Python
            if (0 <= i < self.no_of_rows) and (0 <= j < self.no_of_cols):
                result.append(Point(row=i, col=j))
            #
        #
        return result

    def start(self) -> None:
        visited: set[Point] = set()
        visible: deque[Point] = deque([self.start_point])
        # distance of a point from the start point (S)
        distances: dict[Point, int] = {self.start_point: 0}

        while visible:
            first: Point = visible.popleft()
            for nb in self.get_neighbors(first):
                if nb in visited:
                    continue
                # else
                visible.append(nb)
                distances[nb] = distances[first] + 1
            #
            visited.add(first)
        #
        # self.debug(visited, visible, distance)
        # input("Press Enter...")
        result = max(distances.values())
        print(result)

    def debug(self, visited, visible, distance) -> None:
        print("visited:")
        print(visited)
        print("---")
        print("visible:")
        print(visible)
        print("distances:")
        print(distance)
        print("==========")


def main() -> None:
    # g = Grid("example1.txt", "F")  # 4
    # g = Grid("example2.txt", "F")  # 8
    g = Grid("input.txt", "|")

    g.start()

    # g.debug()


##############################################################################

if __name__ == "__main__":
    main()
