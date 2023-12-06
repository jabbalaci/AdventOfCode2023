#!/usr/bin/env python3

import helper
import intervals


class MyRange:
    def __init__(self, line: str) -> None:
        parts = [int(n) for n in line.split()]
        self.dest_range_start = parts[0]
        self.src_range_start = parts[1]
        self.diff = self.dest_range_start - self.src_range_start
        self.range_length = parts[2]
        start, end = self.src_range_start, self.src_range_start + self.range_length - 1
        self.src_interval = [start, end]
        start, end = self.dest_range_start, self.dest_range_start + self.range_length - 1
        self.dest_interval = [start, end]

    def process(self, value: int) -> int:
        start, end = self.src_range_start, self.src_range_start + self.range_length - 1
        if start <= value <= end:
            diff = value - self.src_range_start
            return self.dest_range_start + diff
        # else
        return -1

    def __str__(self) -> str:
        # return "{}, {}, {}".format(self.dest_range_start, self.src_range_start, self.range_length)
        return "{}, {}".format(self.dest_interval, self.src_interval)


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

    def debug(self):
        print(self.name)
        for r in self.ranges:
            print(r)
        #
        print("---")


class Garden:
    def __init__(self, fname: str) -> None:
        parts: list[str] = helper.read(fname).strip().split("\n\n")
        part1: str = parts[0]
        part2: list[str] = parts[1:]
        self.seeds: list[list[int]] = self.extract_seeds(part1)
        self.converters: list[Converter] = self.get_converters(part2)

    def get_converters(self, parts: list[str]) -> list[Converter]:
        return [Converter(p) for p in parts]

    def extract_seeds(self, line: str) -> list[list[int]]:
        right = line.split(":")[1]
        numbers = [int(n) for n in right.split()]
        groups = [list(t) for t in helper.grouper(numbers, 2)]
        for g in groups:
            g[1] = g[0] + g[1] - 1
        #
        return groups

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
        ll = self.seeds.copy()

        for conv in self.converters:
            ll = helper.merge_intervals(ll)  # optional, also works without it
            # print("# ------------------------------- new converter ---")
            # print("# ll:", ll)
            l1 = []  # outside
            l2 = []  # inside
            for r in conv.ranges:
                # print("> new rule")
                rule = r.src_interval
                for intv in ll:
                    # print(
                    #     "##### intv:",
                    #     intv,
                    #     "; rule:",
                    #     rule,
                    # )
                    d = intervals.match(rule, intv)
                    l1.extend(d["outside"])
                    for inner in d["inside"]:
                        a, b = inner
                        shifted = [a + r.diff, b + r.diff]
                        l2.append(shifted)
                    #
                    # print("# L1:", l1)
                    # print("# L2:", l2)
                    # input("Press ENTER...")
                #
                ll = l1.copy()
                l1.clear()
            #
            ll.extend(l2)
        #
        # print("end list:", ll)
        result = min([intv[0] for intv in ll])
        print(result)

    def debug(self) -> None:
        for conv in self.converters:
            conv.debug()


def main() -> None:
    # fname = "example.txt"
    fname = "input.txt"

    g = Garden(fname)

    g.start()

    # g.debug()


##############################################################################

if __name__ == "__main__":
    main()
