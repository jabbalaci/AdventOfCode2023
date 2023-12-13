#!/usr/bin/env python3

import helper


class Pattern:
    def __init__(self, pattern: str) -> None:
        self.lines: list[str] = pattern.splitlines()
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

    def value(self) -> int:
        vls = self.find_vertical_lines()
        if vls:
            for vl in vls:
                is_symmetric = self.expand_vertically(vl)
                if is_symmetric:
                    return vl[0] + 1
                #
            #
        #
        hls = self.find_horizontal_lines()
        assert hls
        for hl in hls:
            is_symmetric = self.expand_horizonally(hl)
            if is_symmetric:
                return 100 * (hl[0] + 1)
            #
        #
        assert False, "We should never get here"

    def __str__(self) -> str:
        return "\n".join(self.lines)


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
        #
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
