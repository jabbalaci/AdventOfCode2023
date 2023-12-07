#!/usr/bin/env python3


import functools
import itertools
from collections import Counter
from enum import Enum, auto
from pprint import pprint

import helper

char = str

CARDS = "23456789TJQKA"  # leftmost: weakest, rightmost: strongest


class HandType(Enum):
    FIVE_OF_A_KIND = auto()
    FOUR_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    THREE_OF_A_KIND = auto()
    TWO_PAIR = auto()
    ONE_PAIR = auto()
    HIGH_CARD = auto()


def get_type(hand: str) -> HandType:
    kinds: set[char] = set(hand)
    cardinality: int = len(kinds)

    if cardinality == 1:
        return HandType.FIVE_OF_A_KIND
    elif cardinality == 2:
        tmp = sorted(Counter(hand).values())
        if tmp == [1, 4]:
            return HandType.FOUR_OF_A_KIND
        elif tmp == [2, 3]:
            return HandType.FULL_HOUSE
        else:
            assert False, "We should never get here (card. 2)"
    elif cardinality == 3:
        tmp = sorted(Counter(hand).values())
        if tmp == [1, 1, 3]:
            return HandType.THREE_OF_A_KIND
        elif tmp == [1, 2, 2]:
            return HandType.TWO_PAIR
        else:
            assert False, "We should never get here (card. 3)"
    elif cardinality == 4:
        return HandType.ONE_PAIR
    elif cardinality == 5:
        return HandType.HIGH_CARD
    else:
        assert False, "We should never get here"


class Game:
    def __init__(self, lines: list[str]) -> None:
        self.hands: list[str] = []  # will be set later
        self.bids: dict[str, int] = {}  # will be set later
        #
        self.parse(lines)

    def start(self) -> None:
        self.buckets: dict[HandType, list[str]] = self.get_buckets(self.hands)
        self.sort_buckets()
        self.calculate_result()

    def calculate_result(self) -> None:
        my_chain = itertools.chain(
            self.buckets.get(HandType.HIGH_CARD, []),
            self.buckets.get(HandType.ONE_PAIR, []),
            self.buckets.get(HandType.TWO_PAIR, []),
            self.buckets.get(HandType.THREE_OF_A_KIND, []),
            self.buckets.get(HandType.FULL_HOUSE, []),
            self.buckets.get(HandType.FOUR_OF_A_KIND, []),
            self.buckets.get(HandType.FIVE_OF_A_KIND, []),
        )
        total = 0
        for rank, hand in enumerate(my_chain, start=1):
            bid = self.bids[hand]
            total += bid * rank
        #
        print(total)

    def my_cmp(self, a: str, b: str) -> int:
        for i in range(len(a)):
            c1 = a[i]
            c2 = b[i]
            if c1 == c2:
                continue
            # else, if they're different
            pos1 = CARDS.find(c1)
            assert pos1 > -1
            pos2 = CARDS.find(c2)
            assert pos2 > -1
            if pos1 < pos2:
                return -1
            if pos1 > pos2:
                return 1
        # endfor
        return 0

    def sort_buckets(self) -> None:
        for li in self.buckets.values():
            # print("# before:", li)
            li.sort(key=functools.cmp_to_key(self.my_cmp))
            # print("# after:", li)
            # print("---")

    def get_buckets(self, hands: list[str]) -> dict:
        d: dict[HandType, list[str]] = {}
        for hand in hands:
            _type = get_type(hand)
            if _type not in d:
                d[_type] = []
            #
            d[_type].append(hand)
        #
        return d

    def parse(self, lines: list[str]) -> None:
        hands: list[str] = []
        bids: dict[str, int] = {}
        for line in lines:
            left, r = line.split()
            right = int(r)
            hands.append(left)
            bids[left] = right
        #
        self.hands = hands
        self.bids = bids

    def debug(self) -> None:
        # print(self.hands)
        # print(self.bids)
        # pprint(self.buckets)
        pass


def main() -> None:
    # lines = helper.read_lines("example.txt")
    lines = helper.read_lines("input.txt")

    g = Game(lines)

    g.start()

    # g.debug()


##############################################################################

if __name__ == "__main__":
    main()
