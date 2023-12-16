#!/usr/bin/env python3


import copy
from collections import deque
from enum import Enum
from typing import NamedTuple

import helper

# ----------------------------------------------------------------------------

char = str

GridType = list[list[char]]


class Dir(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


class Point(NamedTuple):
    row: int
    col: int


TURN_LEFT = [Dir.UP, Dir.LEFT, Dir.DOWN, Dir.RIGHT, Dir.UP]
TURN_RIGHT = [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT, Dir.UP]

dummy_point = Point(-1, -1)
dummy_dir = Dir.UP

# ----------------------------------------------------------------------------


class LightBeam:
    """A lightbeam's head has a position (row, col) and a direction."""

    def __init__(self, row: int, col: int, direction: Dir, parent: "Grid") -> None:
        self.row = row
        self.col = col
        self.direction = direction
        self.parent: Grid = parent

    def get_new_point(self, to_where: Dir) -> Point:
        row, col = self.row, self.col
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

    def turn_left(self) -> Dir:
        idx = TURN_LEFT.index(self.direction)
        return TURN_LEFT[idx + 1]

    def turn_right(self) -> Dir:
        idx = TURN_RIGHT.index(self.direction)
        return TURN_RIGHT[idx + 1]

    def get_new_points(self, to_where: Dir) -> list["LightBeam"]:
        result: list[LightBeam] = []
        curr_char: char = self.parent.lines[self.row][self.col]

        if curr_char == ".":
            np = self.get_new_point(to_where)
            result.append(LightBeam(np.row, np.col, self.direction, self.parent))
        elif curr_char == "|":
            if self.direction in (Dir.LEFT, Dir.RIGHT):
                result.append(LightBeam(self.row, self.col, Dir.UP, self.parent))
                result.append(LightBeam(self.row, self.col, Dir.DOWN, self.parent))
            else:  # Dir.UP or Dir.DOWN
                np = self.get_new_point(self.direction)
                result.append(LightBeam(np.row, np.col, self.direction, self.parent))
            #
        elif curr_char == "-":
            if self.direction in (Dir.UP, Dir.DOWN):
                result.append(LightBeam(self.row, self.col, Dir.LEFT, self.parent))
                result.append(LightBeam(self.row, self.col, Dir.RIGHT, self.parent))
            else:  # Dir.LEFT or Dir.RIGHT
                np = self.get_new_point(self.direction)
                result.append(LightBeam(np.row, np.col, self.direction, self.parent))
            #
        elif (curr_char == "/") or (curr_char == "\\"):
            if curr_char == "/":
                if self.direction in (Dir.RIGHT, Dir.LEFT):
                    new_dir = self.turn_left()
                else:
                    new_dir = self.turn_right()
                #
            else:  # "\\"
                if self.direction in (Dir.RIGHT, Dir.LEFT):
                    new_dir = self.turn_right()
                else:
                    new_dir = self.turn_left()
                #
            #
            np = self.get_new_point(new_dir)
            result.append(LightBeam(np.row, np.col, new_dir, self.parent))
        #
        return result

    def is_inside(self, lb: "LightBeam") -> bool:
        return (0 <= lb.row < self.parent.no_of_rows) and (0 <= lb.col < self.parent.no_of_cols)

    def move(self) -> list["LightBeam"]:
        result: list["LightBeam"] = []

        new_lightbeams: list[LightBeam] = self.get_new_points(self.direction)
        for nlb in new_lightbeams:
            if self.is_inside(nlb):
                result.append(nlb)
            #
        #
        return result

    def __hash__(self) -> int:
        return hash((self.row, self.col, self.direction))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LightBeam):
            return NotImplemented
        return (
            (self.row == other.row)
            and (self.col == other.col)
            and (self.direction == other.direction)
        )


# ----------------------------------------------------------------------------


class Grid:
    def __init__(self, fname: str, start_point: Point = dummy_point, dir: Dir = dummy_dir) -> None:
        self.lines: GridType = [list(line) for line in helper.read_lines(fname)]
        start_beam = LightBeam(0, 0, Dir.RIGHT, self)
        if start_point != dummy_point:
            start_beam = LightBeam(start_point.row, start_point.col, dir, self)
        #
        self.lightbeams: deque[LightBeam] = deque([start_beam])
        self.visited: set[LightBeam] = set()
        self.no_of_rows: int = len(self.lines)
        self.no_of_cols: int = len(self.lines[0])

    def start(self) -> None:
        while self.lightbeams:  # while not empty
            curr: LightBeam = self.lightbeams.popleft()
            if curr in self.visited:
                continue
            # else
            self.visited.add(curr)
            new_lightbeams = curr.move()
            self.lightbeams.extend(new_lightbeams)
            #
            # self.show()
            # input("Press ENTER to continue...")
        #

    def get_result(self) -> int:
        collect: set[Point] = set()

        for p in self.visited:
            new = Point(row=p.row, col=p.col)
            collect.add(new)
        #
        return len(collect)

    def show(self) -> None:
        lines = copy.deepcopy(self.lines)
        #
        for lb in self.visited:
            old = lines[lb.row][lb.col]
            if old == ".":
                new = lb.direction.value
                lines[lb.row][lb.col] = new
            elif old.isdigit():
                value = int(old)
                lines[lb.row][lb.col] = str(value + 1)
        #
        for line in lines:
            print("".join(line))


# ----------------------------------------------------------------------------


def main():
    # fname = "example.txt"
    fname = "input.txt"

    g = Grid(fname)
    no_of_rows, no_of_cols = g.no_of_rows, g.no_of_cols

    # not too optimal to read the file each time but it works :)
    collect: list[int] = []
    for col in range(no_of_cols):
        g = Grid(fname, Point(row=0, col=col), Dir.DOWN)
        g.start()
        collect.append(g.get_result())
        #
        g = Grid(fname, Point(row=no_of_rows - 1, col=col), Dir.UP)
        g.start()
        collect.append(g.get_result())
    #
    for row in range(no_of_rows):
        g = Grid(fname, Point(row=row, col=0), Dir.RIGHT)
        g.start()
        collect.append(g.get_result())
        #
        g = Grid(fname, Point(row=row, col=no_of_cols - 1), Dir.LEFT)
        g.start()
        collect.append(g.get_result())
    #
    result = max(collect)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
