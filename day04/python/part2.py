#!/usr/bin/env python3

import helper


class Pair:
    def __init__(self, winning_numbers: int) -> None:
        self.winning_numbers: int = winning_numbers
        self.copies = 1

    def __repr__(self) -> str:
        return f"({self.winning_numbers}, {self.copies})"


class Card:
    def __init__(self, numbers: str) -> None:
        self.numbers: str = numbers

    def value(self) -> int:
        left, right = self.numbers.split(" | ")

        left_numbers = {int(n) for n in left.split()}
        right_numbers = {int(n) for n in right.split()}
        common = left_numbers.intersection(right_numbers)

        return len(common)


class Game:
    def __init__(self, lines: list[str]) -> None:
        d: dict[int, Pair] = {}
        for line in lines:
            left, right = line.split(":")
            _id = int(left.split()[-1])
            value = Card(right).value()
            d[_id] = Pair(value)
        #
        self.cards = d

    def start(self) -> None:
        total = 0
        for _id in sorted(self.cards):
            # print("# before:")
            # print(self.cards)

            pair: Pair = self.cards[_id]
            value: int = pair.winning_numbers
            for i in range(value):
                next_id: int = _id + i + 1
                obj: None | Pair = self.cards.get(next_id)
                if not obj:
                    break
                # else
                obj.copies += pair.copies
            #
            total += pair.copies
            pair.copies = 0
            #
            # print("# after:")
            # print(self.cards)
            # print("total:", total)
            # print("---")
            # input("Press Enter...")
        #
        print(total)


def main() -> None:
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    g = Game(lines)
    g.start()


##############################################################################

if __name__ == "__main__":
    main()
