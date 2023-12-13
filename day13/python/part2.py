#!/usr/bin/env python3

from enum import Enum, auto
from typing import NamedTuple

import helper

# ----------------------------------------------------------------------------


class ReflectionType(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


# ----------------------------------------------------------------------------


class Reflection(NamedTuple):
    pos1: int
    pos2: int
    type: ReflectionType


# ----------------------------------------------------------------------------


class Pattern:
    def __init__(self, pattern: str) -> None:
        self.lines: list[list[str]] = [list(line) for line in pattern.splitlines()]
        self.no_of_rows: int = len(self.lines)
        self.no_of_cols: int = len(self.lines[0])

    def same_columns(self, col1: int, col2: int) -> bool:
        for line in self.lines:
            if line[col1] != line[col2]:
                return False
            #
        #
        return True

    def find_vertical_lines(self) -> list[tuple[int, int]] | None:
        found: list[tuple[int, int]] = []
        for col in range(0, self.no_of_cols - 2 + 1):
            col1 = col
            col2 = col + 1
            if self.same_columns(col1, col2):
                found.append((col1, col2))
            #
        #
        return found

    def same_rows(self, row1: int, row2: int) -> bool:
        return self.lines[row1] == self.lines[row2]

    def find_horizontal_lines(self) -> list[tuple[int, int]] | None:
        found: list[tuple[int, int]] = []
        for row in range(0, self.no_of_rows - 2 + 1):
            row1 = row
            row2 = row + 1
            if self.same_rows(row1, row2):
                found.append((row1, row2))
            #
        #
        return found

    def expand_vertically(self, vl: tuple[int, int]) -> bool:
        col1, col2 = vl
        while True:
            col1 -= 1
            col2 += 1
            if (col1 < 0) or (col2 >= self.no_of_cols):
                return True
            # else
            if not self.same_columns(col1, col2):
                break
            #
        #
        return False

    def expand_horizonally(self, hl: tuple[int, int]) -> bool:
        row1, row2 = hl
        while True:
            row1 -= 1
            row2 += 1
            if (row1 < 0) or (row2 >= self.no_of_rows):
                return True
            # else
            if not self.same_rows(row1, row2):
                break
            #
        #
        return False

    def try_to_process(self, o_refl: Reflection | None) -> tuple[int, Reflection]:
        vls = self.find_vertical_lines()
        if vls:
            for vl in vls:
                if o_refl:
                    curr_refl = Reflection(vl[0], vl[1], ReflectionType.VERTICAL)
                    if curr_refl == o_refl:
                        continue
                    #
                #
                is_symmetric = self.expand_vertically(vl)
                if is_symmetric:
                    return vl[0] + 1, Reflection(vl[0], vl[1], ReflectionType.VERTICAL)
                #
            #
        #
        hls = self.find_horizontal_lines()
        if hls:
            for hl in hls:
                if o_refl:
                    curr_refl = Reflection(hl[0], hl[1], ReflectionType.HORIZONTAL)
                    if curr_refl == o_refl:
                        continue
                    #
                #
                is_symmetric = self.expand_horizonally(hl)
                if is_symmetric:
                    return 100 * (hl[0] + 1), Reflection(hl[0], hl[1], ReflectionType.HORIZONTAL)
                #
        #
        return -1, Reflection(-1, -1, ReflectionType.HORIZONTAL)

    def flip(self, row: int, col: int) -> None:
        self.lines[row][col] = "." if self.lines[row][col] == "#" else "#"

    def value(self) -> int:
        _, original_reflection = self.try_to_process(None)

        for row, line in enumerate(self.lines):
            for col, _ in enumerate(line):
                self.flip(row, col)
                v, refl = self.try_to_process(original_reflection)
                if (v > -1) and (refl != original_reflection):
                    return v
                #
                self.flip(row, col)
            #
        #
        assert False, "We should never get here"

    def __str__(self) -> str:
        return "\n".join("".join(line) for line in self.lines)


# ----------------------------------------------------------------------------


class PatternCollection:
    def __init__(self, fname: str) -> None:
        self.patterns: list[Pattern] = []
        content: str = helper.read(fname)
        for p in content.split("\n\n"):
            self.patterns.append(Pattern(p))

    def start(self) -> None:
        total = 0
        for p in self.patterns:
            total += p.value()
            # print(".", end="", flush=True)
        #
        # print()
        print(total)

    def debug(self) -> None:
        for p in self.patterns:
            print(p)
            print("---")


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example.txt"
    fname = "input.txt"

    pc = PatternCollection(fname)

    pc.start()

    # pc.debug()


##############################################################################

if __name__ == "__main__":
    main()
