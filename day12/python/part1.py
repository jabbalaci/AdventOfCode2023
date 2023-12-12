#!/usr/bin/env python3

import helper


class Springs:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def process(self, line: str) -> int:
        result = 0
        # print(line)
        left, right = line.split()
        goal: list[int] = [int(n) for n in right.split(",")]
        template = list(left)
        length = template.count("?")
        for n in range(2**length):
            binary: str = bin(n)[2:].zfill(length).replace("0", ".").replace("1", "#")
            found = 0
            current = template.copy()
            for idx in range(len(current)):
                c = current[idx]
                if c == "?":
                    current[idx] = binary[found]
                    found += 1
                #
            #
            new = "".join(current).replace(".", " ")
            # print(new)
            length_of_pieces = [len(p) for p in new.split()]
            if length_of_pieces == goal:
                result += 1
            #
        #
        return result

    def start(self) -> None:
        total = 0
        for line in self.lines:
            value: int = self.process(line)
            # print(value)
            total += value
            print(".", end="", flush=True)
        #
        print()
        print(total)

    def debug(self):
        for line in self.lines:
            print(line)


def main():
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    sp = Springs(lines)

    sp.start()

    # sp.debug()


##############################################################################

if __name__ == "__main__":
    main()
