#!/usr/bin/env python3

import re

import helper


def hash_it(s: str) -> int:
    total = 0

    for c in s:
        total += ord(c)
        total *= 17
        total %= 256

    return total


# ----------------------------------------------------------------------------


class Box:
    def __init__(self, _id: int) -> None:
        self._id = _id
        self.d: dict[str, int] = {}

    def remove(self, lens: str) -> None:
        if lens in self.d:
            del self.d[lens]

    def add(self, k: str, v: int) -> None:
        self.d[k] = v

    def is_empty(self) -> bool:
        return len(self.d) == 0

    def value(self) -> int:
        total = 0
        box_number = self._id + 1
        cnt = 1
        for v in self.d.values():
            total += box_number * cnt * v
            cnt += 1
        #
        return total

    def __str__(self) -> str:
        return str(self.d)


# ----------------------------------------------------------------------------


class Facility:
    def __init__(self, fname: str) -> None:
        line: str = helper.read(fname).strip()
        self.parts: list[str] = line.split(",")
        #
        self.boxes: list[Box] = []
        for i in range(256):
            self.boxes.append(Box(i))
        #

    def process(self, part: str) -> None:
        left, right = re.split(r"-|=", part)
        idx = hash_it(left)
        if "-" in part:
            self.boxes[idx].remove(left)
        elif "=" in part:
            self.boxes[idx].add(left, int(right))
        else:
            assert False, "We should never get here"

    def start(self) -> None:
        for part in self.parts:
            self.process(part)
        #
        result = 0
        for box in self.boxes:
            result += box.value()
        #
        print(result)

    def debug(self) -> None:
        for box in self.boxes:
            if not box.is_empty():
                print(box)


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example.txt"
    fname = "input.txt"

    f = Facility(fname)

    f.start()

    # f.debug()


##############################################################################

if __name__ == "__main__":
    main()
