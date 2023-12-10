#!/usr/bin/env python3

"""
For this I had no idea how to approach, so I looked after it.

Textual hint: https://old.reddit.com/r/adventofcode/comments/18ey1s7
"""

import sys
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

    def start(self) -> None:
        self.loop: set[Point] = self.find_loop()
        self.simplify()
        self.find_inside_and_outside()

    def simplify(self) -> None:
        """
        Change any character that is not in the loop to '.'
        1) it makes visualization more readable (less noise)
        2) it's simpler to decide if a position is inside or outside
        """
        for i in range(len(self.lines)):
            curr_row = self.lines[i]
            new_row = ""
            for col, c in enumerate(curr_row):
                p = Point(row=i, col=col)
                if p in self.loop:
                    new_row += c
                else:
                    new_row += "."
                #
            #
            self.lines[i] = new_row
        #

    def find_inside_and_outside(self) -> None:
        outside: set[Point] = set()
        inside: set[Point] = set()
        #
        for row, line in enumerate(self.lines):
            for col, c in enumerate(line):
                if c != ".":
                    continue
                # else, if it's a '.'
                right_side = ""
                for i in range(col + 1, len(line)):
                    p = Point(row=row, col=i)
                    if p not in self.loop:
                        continue
                    # else, if p is in the loop
                    ch = line[i]
                    if ch == "S":
                        ch = self.start_char
                    #
                    right_side += ch
                #
                # print("{}: {}".format(Point(row, col), right))
                right_side = right_side.replace("-", "")
                right_side = right_side.replace("FJ", "|")
                right_side = right_side.replace("L7", "|")
                right_side = right_side.replace("F7", "")
                right_side = right_side.replace("LJ", "")
                for c in right_side:
                    assert c == "|", f"# c is: {c}; line is: {line}; right is: {right_side}"
                #
                p = Point(row, col)
                if len(right_side) % 2 == 0:
                    outside.add(p)
                else:
                    inside.add(p)
                #
            # endfor col
        # endfor row
        self.inside = inside
        self.outside = outside

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

    def find_loop(self) -> set[Point]:
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
        return visited

    def draw_map(self) -> None:
        d = {
            "F": "┌",
            "7": "┐",
            "L": "└",
            "J": "┘",
            "|": "|",
            "-": "-",
            "S": "S",
        }
        for row, line in enumerate(self.lines):
            for col, c in enumerate(line):
                p = Point(row=row, col=col)
                if p in self.outside:
                    sys.stdout.write("O")
                elif p in self.inside:
                    sys.stdout.write("I")
                elif p in self.loop:
                    sys.stdout.write(d[c])
                else:
                    sys.stdout.write(c)
                #
            #
            print()
        #

    def debug(self) -> None:
        d = {
            "F": "┌",
            "7": "┐",
            "L": "└",
            "J": "┘",
            "|": "|",
            "-": "-",
            "S": "S",
        }
        for line in self.lines:
            for c in line:
                if c in d:
                    sys.stdout.write(d[c])
                else:
                    sys.stdout.write(c)
                #
            #
            print()
        #


def main() -> None:
    # g = Grid("example1.txt", "F")  # 1
    # g = Grid("example2.txt", "F")  # 1
    g = Grid("input.txt", "|")

    # g = Grid("replace/part2-1.txt", "F")  # 4
    # g = Grid("replace/part2-2.txt", "F")  # 4
    # g = Grid("replace/part2-3.txt", "F")  # 8
    # g = Grid("replace/part2-4.txt", "7")  # 10

    g.start()

    # g.draw_map()
    # print("---")

    # g.debug()
    # print("---")

    result = len(g.inside)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
