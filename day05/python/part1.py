#!/usr/bin/env python3

import helper


class MyRange:
    def __init__(self, line: str) -> None:
        parts = [int(n) for n in line.split()]
        self.dest_range_start = parts[0]
        self.src_range_start = parts[1]
        self.range_length = parts[2]

    def process(self, value: int) -> int:
        start, end = self.src_range_start, self.src_range_start + self.range_length - 1
        if start <= value <= end:
            diff = value - self.src_range_start
            return self.dest_range_start + diff
        # else
        return -1

    def __str__(self) -> str:
        return "{}, {}, {}".format(self.dest_range_start, self.src_range_start, self.range_length)


class Converter:
    def __init__(self, content: str) -> None:
        lines = content.splitlines()
        self.name = lines[0].rstrip(":")
        self.ranges = [MyRange(r) for r in lines[1:]]

    def process(self, value: int) -> int:
        for r in self.ranges:
            result = r.process(value)
            if result > -1:
                return result
            #
        #
        # if value wasn't found in any range:
        return value


class Garden:
    def __init__(self, fname: str) -> None:
        parts: list[str] = helper.read(fname).strip().split("\n\n")
        part1: str = parts[0]
        part2: list[str] = parts[1:]
        self.seeds: list[int] = self.extract_seeds(part1)
        self.converters: list[Converter] = self.get_converters(part2)

    def get_converters(self, parts: list[str]) -> list[Converter]:
        return [Converter(p) for p in parts]

    def extract_seeds(self, line: str) -> list[int]:
        right = line.split(":")[1]
        return [int(n) for n in right.split()]

    def process(self, seed: int) -> int:
        value = seed
        for conv in self.converters:
            # print("# before:", value)
            value = conv.process(value)
            # print("# after:", value)
            # print("---")
        #
        return value

    def start(self) -> None:
        values = [self.process(seed) for seed in self.seeds]
        result = min(values)
        print(result)

    def debug(self) -> None:
        print("# seeds:", self.seeds)


def main() -> None:
    # fname = "example.txt"
    fname = "input.txt"

    g = Garden(fname)

    g.start()

    # g.debug()


##############################################################################

if __name__ == "__main__":
    main()
