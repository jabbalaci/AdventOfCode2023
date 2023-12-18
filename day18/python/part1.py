#!/usr/bin/env python3

from typing import NamedTuple

import helper


class Point(NamedTuple):
    row: int
    col: int


# from https://web.archive.org/web/20100405070507/http://valis.cs.uiuc.edu/~sariel/research/CG/compgeom/msg00831.html
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
        points.append(points[0])  # connect the last and the first point (for the perimeter)
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
            _dir, v, color = line.split()
            value = int(v)
            if _dir == "R":
                j += value
            elif _dir == "L":
                j -= value
            elif _dir == "U":
                i -= value
            elif _dir == "D":
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
