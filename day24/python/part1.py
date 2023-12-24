#!/usr/bin/env python3

import itertools
from typing import NamedTuple

import helper
from helper import sign

EXAMPLE, REAL_INPUT = range(2)


class Point(NamedTuple):
    x: float
    y: float


class Line(NamedTuple):
    a: Point
    b: Point


# from https://stackoverflow.com/questions/20677795
def line_intersection(line1: Line, line2: Line) -> Point:
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception("lines do not intersect")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return Point(x, y)


# ----------------------------------------------------------------------------


class Processor:
    def __init__(self, data: tuple[str, int]) -> None:
        fname, _type = data
        self.interval = (7, 27)  # for the example
        if _type == REAL_INPUT:
            self.interval = (200000000000000, 400000000000000)  # for the real stuff
        #
        self.lines: list[Line] = self.parse(helper.read_lines(fname))

    def same_direction(self, a: Point, b: Point, c: Point) -> bool:
        x1 = b.x - a.x
        y1 = b.y - a.y
        x2 = c.x - b.x
        y2 = c.y - b.y
        return sign(x2) == sign(x1) and sign(y2) == sign(y1)

    def start(self) -> None:
        lo, hi = self.interval
        cnt = 0
        for line1, line2 in itertools.combinations(self.lines, 2):
            try:
                p = line_intersection(line1, line2)
                # print(line1, line2, p)
                if lo <= p.x <= hi and lo <= p.y <= hi:
                    future1 = self.same_direction(line1.a, line1.b, p)
                    future2 = self.same_direction(line2.a, line2.b, p)
                    # print(future1, future2)
                    if future1 and future2:
                        cnt += 1
                        # print("+1")
                    #
                else:
                    # print("outside")
                    pass
            except Exception:
                # print("They are parallel")
                pass
            #
            # print("---")
        #
        print(cnt)

    def parse(self, str_lines: list[str]) -> list[Line]:
        result: list[Line] = []

        for line in str_lines:
            l, r = line.split(" @ ")
            left = [int(n) for n in l.split(",")]
            right = [int(n) for n in r.split(",")]
            p1 = Point(x=left[0], y=left[1])
            p2 = Point(x=p1.x + right[0], y=p1.y + right[1])
            result.append(Line(p1, p2))
        #
        return result

    def debug(self, lines) -> None:
        for line in lines:
            print(line)


# ----------------------------------------------------------------------------


def main():
    # data = ("example.txt", EXAMPLE)
    data = ("input.txt", REAL_INPUT)

    p = Processor(data)

    p.start()

    # p.debug()


##############################################################################

if __name__ == "__main__":
    main()
