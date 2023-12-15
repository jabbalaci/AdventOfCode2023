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

    def can_go(self, row: int, col: int, to_where: Dir) -> bool:
        result = False
        new_pos: Point = self.get_new_point(row, col, to_where)

        if to_where == Dir.UP:
            if (new_pos.row >= 0) and (self.lines[new_pos.row][new_pos.col] == "."):
                result = True
            #
        elif to_where == Dir.LEFT:
            if (new_pos.col >= 0) and (self.lines[new_pos.row][new_pos.col] == "."):
                result = True
            #
        elif to_where == Dir.DOWN:
            if (new_pos.row < self.no_of_rows) and (self.lines[new_pos.row][new_pos.col] == "."):
                result = True
            #
        elif to_where == Dir.RIGHT:
            if (new_pos.col < self.no_of_cols) and (self.lines[new_pos.row][new_pos.col] == "."):
                result = True
            #
        else:
            assert False, "We should never get here"

        return result

    def get_new_point(self, row: int, col: int, to_where: Dir) -> Point:
        if to_where == Dir.UP:
            return Point(row=row - 1, col=col)
        if to_where == Dir.LEFT:
            return Point(row=row, col=col - 1)
        if to_where == Dir.DOWN:
            return Point(row=row + 1, col=col)
        if to_where == Dir.RIGHT:
            return Point(row=row, col=col + 1)
        #
        assert False, "We should never get here"

    def try_to_move(self, i: int, j: int, to_where: Dir) -> bool:
        moved = False
        assert self.lines[i][j] == "O"
        row, col = i, j

        if self.can_go(i, j, to_where):
            new_pos: Point = self.get_new_point(row, col, to_where)
            self.lines[row][col], self.lines[new_pos.row][new_pos.col] = (
                self.lines[new_pos.row][new_pos.col],
                self.lines[row][col],
            )
            moved = True
        #
        return moved

    def tilt(self, to_where: Dir) -> None:
        moved = True
        while moved:
            moved = False
            for row, line in enumerate(self.lines):
                for col, c in enumerate(line):
                    if c == "O":
                        did_it_move = self.try_to_move(row, col, to_where)
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

    def cycle(self) -> None:
        self.tilt(Dir.UP)
        self.tilt(Dir.LEFT)
        self.tilt(Dir.DOWN)
        self.tilt(Dir.RIGHT)

    def start(self) -> None:
        collect = []
        cnt = 1
        for i in range(300):
            self.cycle()
            result = self.calculate_result()
            print(f"iter: {cnt}, value: {result}")
            collect.append(result)
            cnt += 1
        #
        print(collect)
        # self.debug()
        # result = self.calculate_result()
        # print(result)

    def debug(self, li) -> None:
        for line in li:
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
