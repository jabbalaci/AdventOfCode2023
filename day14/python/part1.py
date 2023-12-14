#!/usr/bin/env python3

from enum import Enum, auto
from typing import NamedTuple

import helper

# ----------------------------------------------------------------------------


class Point(NamedTuple):
    row: int
    col: int


# ----------------------------------------------------------------------------


class Dir(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


# ----------------------------------------------------------------------------


class Grid:
    def __init__(self, fname: str) -> None:
        self.lines: list[list[str]] = [list(line) for line in helper.read_lines(fname)]
        self.no_of_rows: int = len(self.lines)
        self.no_of_cols: int = len(self.lines[0])

    def can_go_up(self, row: int, col: int) -> bool:
        result = False

        pos_up = Point(row=row - 1, col=col)
        if (pos_up.row >= 0) and (self.lines[pos_up.row][pos_up.col] == "."):
            result = True

        return result

    def try_to_move_up(self, i: int, j: int) -> bool:
        moved = False

        c = self.lines[i][j]
        assert c == "O"
        if self.can_go_up(i, j):
            self.lines[i][j], self.lines[i - 1][j] = self.lines[i - 1][j], self.lines[i][j]
            moved = True

        return moved

    def tilt_up(self) -> None:
        moved = True
        while moved:
            moved = False
            for row, line in enumerate(self.lines):
                for col, c in enumerate(line):
                    if c == "O":
                        did_it_move = self.try_to_move_up(row, col)
                        if did_it_move:
                            moved = True
                        #
                    #
                #
            #
        #

    def calculate_result(self) -> int:
        total = 0
        for row, line in enumerate(self.lines):
            line_value = self.no_of_rows - row
            for c in line:
                if c == "O":
                    total += line_value
                #
            #
        #
        return total

    def start(self) -> None:
        self.tilt_up()
        # self.debug()
        result = self.calculate_result()
        print(result)

    def debug(self) -> None:
        for line in self.lines:
            print("".join(line))
            # print(line)


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example.txt"
    fname = "input.txt"

    g = Grid(fname)

    g.start()

    # g.debug()


##############################################################################

if __name__ == "__main__":
    main()
