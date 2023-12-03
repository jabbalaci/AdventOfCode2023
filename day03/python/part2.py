#!/usr/bin/env python3

# i: row
# j: column

import math

import helper

char = str  # type alias


class Number:
    def __init__(self, text: str, i: int, j: int) -> None:
        self.text: str = text
        # row, column: where this number starts
        self.i: int = i  # row
        self.j: int = j  # column

    def value(self) -> int:
        return int(self.text)

    def is_hit(self, row: int, col: int) -> bool:
        if row == self.i:
            if self.j <= col < self.j + len(self.text):
                return True
            #
        #
        return False

    def __hash__(self) -> int:
        return hash((self.text, self.i, self.j))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Number):
            return NotImplemented
        return (self.text == other.text) and (self.i == other.i) and (self.j == other.j)

    def __str__(self) -> str:
        return f"{self.value()} ({self.i}, {self.j})"

    def __repr__(self) -> str:
        return self.__str__()


class Grid:
    def __init__(self, lines: list[str]) -> None:
        self.lines: list[str] = lines
        self.rows: int = len(lines)
        self.columns: int = len(lines[0])

    def start(self) -> None:
        self.find_numbers()
        result = self.find_result()
        print(result)

    def is_symbol(self, c: char) -> bool:
        if c == "." or c.isdigit():
            return False
        #
        return True

    def get_hit_number(self, row: int, col: int) -> None | Number:
        """Is there a number at this position?"""
        for n in self.numbers:
            if n.is_hit(row, col):
                return n
            #
        #
        return None

    def get_adjacent_numbers(self, i: int, j: int) -> set[Number]:
        neigbors: set[Number] = set()

        top_left_i, top_left_j = i - 1, j - 1
        bottom_right_i, bottom_right_j = i + 1, j + 1
        if top_left_i < 0:
            top_left_i = 0
        if top_left_j < 0:
            top_left_j = 0
        if bottom_right_i >= self.rows:
            bottom_right_i -= 1
        if bottom_right_j >= self.columns:
            bottom_right_j -= 1

        for row in range(top_left_i, bottom_right_i + 1):
            for col in range(top_left_j, bottom_right_j + 1):
                found: None | Number = self.get_hit_number(row, col)
                if found:
                    neigbors.add(found)
                #
            #
        #
        return neigbors

    def find_result(self) -> int:
        total = 0
        for i, line in enumerate(self.lines):
            for j, c in enumerate(line):
                if c == "*":
                    numbers: set[Number] = self.get_adjacent_numbers(i, j)
                    if len(numbers) == 2:
                        total += math.prod([n.value() for n in numbers])
                    #
                #
            #
        #
        return total

    def find_end(self, line: str, j: int) -> int:
        while True:
            j += 1
            if j >= self.columns:
                return self.columns - 1
            # else
            c = line[j]
            if not c.isdigit():
                return j - 1
            #
        #

    def find_numbers(self) -> None:
        numbers: list[Number] = []
        for i, line in enumerate(self.lines):
            j = 0
            while j < self.columns:
                c = line[j]
                if c.isdigit():
                    begin = j
                    end = self.find_end(line, j)  # closed interval
                    n = Number(line[begin : end + 1], i, begin)
                    numbers.append(n)
                    j = end
                #
                j += 1
            #
        #
        self.numbers = numbers

    def debug(self) -> None:
        # for line in self.lines:
        # print(line)
        #
        # print(f"No. of rows: {self.rows}")
        # print(f"No. of cols: {self.columns}")
        for n in self.numbers:
            print(n)


def main() -> None:
    # lines = helper.read_lines("my_example.txt")
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    g = Grid(lines)
    g.start()

    # g.debug()


##############################################################################

if __name__ == "__main__":
    main()
