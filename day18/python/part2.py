#!/usr/bin/env python3

from typing import NamedTuple

import helper


class Point(NamedTuple):
    row: int
    col: int


def my_area(vertices: list[Point]) -> float:
    N = len(vertices)
    area = 0.0
    for i in range(N - 1):
        j = (i + 1) % N
        area = area + vertices[i][0] * vertices[j][1]
        area = area - vertices[i][1] * vertices[j][0]
    #
    return abs(area) / 2


class Grid:
    def __init__(self, fname: str) -> None:
        self.lines = helper.read_lines(fname)

    def get_perimeter(self, points) -> int:
        """
        It also compares the first point (idx: 0) with the last point (idx: -1).

        So the perimeter is calculated correctly even if the first point
        is not repeated in the last position.
        """
        total = 0
        for i in range(len(points)):
            curr = points[i]
            prev = points[i - 1]
            value = abs(curr.row - prev.row) + abs(curr.col - prev.col)
            total += value
        #
        return total

    def start(self) -> None:
        self.d = self.dig()
        points: list[Point] = [k for k in self.d]
        # print(points)
        area: float = my_area(points)
        # print(area)
        perimeter: int = self.get_perimeter(points)
        # print(perimeter)
        result: int = int(area) + (perimeter // 2) + 1
        print(result)

    def dig(self) -> dict:
        i, j = 0, 0
        d = {Point(row=0, col=0): 1}

        for line in self.lines:
            _, _, color = line.split()
            color = color.strip("(#)")
            value = int(color[:-1], 16)
            _dir = color[-1]
            if _dir == "0":  # R
                j += value
            elif _dir == "2":  # L
                j -= value
            elif _dir == "3":  # U
                i -= value
            elif _dir == "1":  # D
                i += value
            else:
                assert False, "We should never get here"
            #
            d[Point(row=i, col=j)] = 1
            #
        #
        return d


def main():
    # fname = "example.txt"
    fname = "input.txt"

    g = Grid(fname)

    g.start()


##############################################################################

if __name__ == "__main__":
    main()
