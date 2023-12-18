#!/usr/bin/env python3

import sys
from pathlib import Path
from pprint import pprint
from typing import NamedTuple


class Point(NamedTuple):
    row: int
    col: int


def read_lines(fname: str) -> list[str]:
    with open(fname) as f:
        return f.read().strip().splitlines()


class Grid:
    def __init__(self, fname: str) -> None:
        self.fname = Path(fname)
        self.lines = read_lines(fname)

    def start(self) -> None:
        self.d = self.dig()
        self.top_left = self.find_top_left()
        self.bottom_right = self.find_bottom_right()

    def find_bottom_right(self) -> Point:
        max_row = max(p.row for p in self.d)
        max_col = max(p.col for p in self.d)
        return Point(row=max_row, col=max_col)

    def find_top_left(self) -> Point:
        min_row = min(p.row for p in self.d)
        min_col = min(p.col for p in self.d)
        return Point(row=min_row, col=min_col)

    def dig(self) -> dict:
        i, j = 0, 0
        d = {Point(row=0, col=0): 1}

        for line in self.lines:
            _dir, value, color = line.split()
            for _ in range(int(value)):
                if _dir == "R":
                    j += 1
                elif _dir == "L":
                    j -= 1
                elif _dir == "U":
                    i -= 1
                elif _dir == "D":
                    i += 1
                else:
                    assert False, "We should never get here"
                #
                d[Point(row=i, col=j)] = 1
            #
        #
        return d

    def show(self) -> None:
        for row in range(self.top_left.row, self.bottom_right.row + 1):
            for col in range(self.top_left.col, self.bottom_right.col + 1):
                if (row, col) not in self.d:
                    sys.stdout.write(".")
                else:
                    sys.stdout.write("#")
                #
            #
            print()
        #

    def create_image_file(self):
        name = self.fname.stem + ".pbm"
        sb = []
        sb.append("P1")
        sb.append(f"# {name}")
        width = self.bottom_right.col - self.top_left.col + 1
        height = self.bottom_right.row - self.top_left.row + 1
        sb.append(f"{width} {height}")
        for row in range(self.top_left.row, self.bottom_right.row + 1):
            line = ""
            for col in range(self.top_left.col, self.bottom_right.col + 1):
                if (row, col) not in self.d:
                    line += "0 "
                else:
                    line += "1 "
                #
            #
            sb.append(line)
        #
        with open(name, "w") as f:
            for line in sb:
                print(line, file=f)
            #
        #
        print(f"{name} was created")

    def debug(self):
        for line in self.lines:
            print(line)


def main():
    fname = "example.txt"
    # fname = "input.txt"

    g = Grid(fname)

    g.start()

    # g.show()
    g.create_image_file()

    # g.debug()


##############################################################################

if __name__ == "__main__":
    main()
