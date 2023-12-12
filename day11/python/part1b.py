#!/usr/bin/env python3

"""
Similar to version 1a, but here we don't do
physical expansion (that'd be too expensive for Part 2).

We simply keep track of the empty rows and empty columns.
"""

import itertools
from typing import NamedTuple

import helper

char = str


class Point(NamedTuple):
    row: int
    col: int


class Expansion:
    def __init__(self, fname: str) -> None:
        ll: list[str] = helper.read_lines(fname)
        self.lines: list[list[char]] = [list(line) for line in ll]
        self.no_of_rows: int = len(self.lines)
        self.no_of_cols: int = len(self.lines[0])

    def process(self) -> list[str]:
        self.expand_rows()
        self.expand_cols()
        #
        return ["".join(line) for line in self.lines]

    def is_empty(self, row_or_col: list[char]) -> bool:
        return all([c == "." for c in row_or_col])

    def collect_empty_rows(self) -> list[int]:
        result: list[int] = []

        for i in range(self.no_of_rows):
            curr: list[str] = self.lines[i]
            if self.is_empty(curr):
                result.append(i)
            #
        #
        return result

    def get_column(self, idx: int) -> list[char]:
        return [line[idx] for line in self.lines]

    def collect_empty_cols(self) -> list[int]:
        result: list[int] = []

        for i in range(self.no_of_cols):
            curr: list[char] = self.get_column(i)
            if self.is_empty(curr):
                result.append(i)
            #
        #
        return result

    def expand_rows(self) -> None:
        self.empty_rows: list[int] = self.collect_empty_rows()
        # empty_row: list[char] = list("." * self.no_of_rows)
        # offset = 0
        # for idx in empty_rows:
        # self.lines.insert(idx + offset, empty_row.copy())
        # offset += 1
        #

    def expand_cols(self) -> None:
        self.empty_cols: list[int] = self.collect_empty_cols()
        # offset = 0
        # for idx in empty_cols:
        # for line in self.lines:
        # line.insert(idx + offset, ".")
        #
        # offset += 1
        #

    def debug(self) -> None:
        for line in self.lines:
            print("".join(line))


# ---------------------------------------------------------------------------


class Universe:
    def __init__(self, fname: str, duplicates: int) -> None:
        # if there's an empty row/column, how many duplicates to add:
        self.duplicates = duplicates - 1
        exp = Expansion(fname)
        self.lines: list[str] = exp.process()
        self.no_of_rows: int = len(self.lines)
        self.no_of_cols: int = len(self.lines[0])
        self.empty_rows: set[int] = set(exp.empty_rows)
        self.empty_cols: set[int] = set(exp.empty_cols)

    def collect_galaxies(self) -> list[Point]:
        result: list[Point] = []

        for i, line in enumerate(self.lines):
            for j, c in enumerate(line):
                if c == "#":
                    p = Point(row=i, col=j)
                    result.append(p)
                #
            #
        #
        return result

    # def distance_between(self, p1: Point, p2: Point) -> int:
    # """Manhattan distance"""
    # return abs(p1.row - p2.row) + abs(p1.col - p2.col)

    def distance_between_v2(self, p1: Point, p2: Point) -> int:
        """modified Manhattan distance (with duplicates)"""
        rows = sorted([p1.row, p2.row])
        cols = sorted([p1.col, p2.col])
        total = 0
        for row in range(rows[0], rows[1]):
            total += 1
            if row in self.empty_rows:
                total += self.duplicates
            #
        #
        for col in range(cols[0], cols[1]):
            total += 1
            if col in self.empty_cols:
                total += self.duplicates
            #
        #
        return total

    def start(self) -> None:
        self.galaxies = self.collect_galaxies()
        self.combinations = itertools.combinations(self.galaxies, 2)

        total = 0
        for p1, p2 in self.combinations:
            total += self.distance_between_v2(p1, p2)
        #
        print(total)

    def debug(self) -> None:
        for line in self.lines:
            print(line)
        #
        # print("---")
        # print(self.galaxies)
        # print("---")
        # for comb in self.combinations:
        # print(comb)
        print("---")
        print(self.empty_rows)
        print(self.empty_cols)


# ---------------------------------------------------------------------------


def main() -> None:
    # u = Universe("example.txt", 2)
    u = Universe("input.txt", 2)

    u.start()

    # u.debug()


##############################################################################

if __name__ == "__main__":
    main()
