#!/usr/bin/env python3

# i: row
# j: column

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

    def __str__(self) -> str:
        return f"{self.value()} ({self.i}, {self.j})"


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

    def find_result(self) -> int:
        total = 0
        for n in self.numbers:
            top_left_i, top_left_j = n.i - 1, n.j - 1
            bottom_right_i, bottom_right_j = n.i + 1, n.j + len(n.text)
            if top_left_i < 0:
                top_left_i = 0
            if top_left_j < 0:
                top_left_j = 0
            if bottom_right_i >= self.rows:
                bottom_right_i -= 1
            if bottom_right_j >= self.columns:
                bottom_right_j -= 1

            stop = False
            for row in range(top_left_i, bottom_right_i + 1):
                for col in range(top_left_j, bottom_right_j + 1):
                    c = self.lines[row][col]
                    if self.is_symbol(c):
                        # print(
                        # "# frame: {},{} {},{}".format(
                        # top_left_i, top_left_j, bottom_right_i, bottom_right_j
                        # )
                        # )
                        # print("# found a value:", n)
                        total += n.value()
                        stop = True
                    # endif
                    if stop:
                        break
                # end inner for
                if stop:
                    break
            # end outer for
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
