#!/usr/bin/env python3

import math
from copy import deepcopy
from pprint import pprint

import helper

# ----------------------------------------------------------------------------


class Machine:
    def __init__(self, fname: str) -> None:
        content: str = helper.read(fname)
        first, _ = content.split("\n\n")
        self.workflows: dict[str, list[str]] = self.parse_workflows(first)

    def parse_workflows(self, text: str) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        lines = text.splitlines()
        for line in lines:
            _id, rest = line.split("{")
            rest = rest.rstrip("}")
            rules = rest.split(",")
            result[_id] = rules
        #
        return result

    def apply_condition(self, d_original: dict, condition: str, negate=False) -> dict:
        d = deepcopy(d_original)

        part = condition[0]
        assert part in "xmas"
        relation = condition[1]
        assert relation in ("><")
        value = int(condition[2:])
        assert 1 <= value <= 4000

        interval = d[part]

        if relation == "<":
            if not negate:  # apply condition
                interval[-1] = value - 1
            else:  # apply the negate of the condition
                interval[0] = value
            #
        else:
            if not negate:  # apply condition
                interval[0] = value + 1
            else:  # apply the negate of the condition
                interval[-1] = value
            #
        #
        return d

    def traverse(self, _id: str, d_original: dict) -> int:
        d = d_original  # doesn't have to be a complete copy yet
        #
        # print(_id)
        # print(d)
        # print("---")
        #
        if _id == "R":
            return 0
        # else
        if _id == "A":
            collect = []
            for a, b in d.values():
                collect.append(b - a + 1)
            #
            return math.prod(collect)  # type: ignore
        # else
        total = 0
        prev_conditions: list[str] = []
        for idx, rule in enumerate(self.workflows[_id]):
            d = deepcopy(d_original)  # complete copy is necessary here
            if ":" in rule:
                curr_condition, target = rule.split(":")
                for cond in prev_conditions:
                    d = self.apply_condition(d, cond, negate=True)
                #
                d = self.apply_condition(d, curr_condition)
                prev_conditions.append(curr_condition)
            else:
                last_index = len(self.workflows[_id]) - 1
                assert idx == last_index  # make sure this is the last "rule"
                target = rule
                for cond in prev_conditions:
                    d = self.apply_condition(d, cond, negate=True)
                #
            #
            total += self.traverse(target, d)
        #
        return total

    def start(self) -> None:
        d = {
            "x": [1, 4000],
            "m": [1, 4000],
            "a": [1, 4000],
            "s": [1, 4000],
        }
        result = self.traverse("in", d)
        print(result)

    def debug(self) -> None:
        pprint(self.workflows)


# ----------------------------------------------------------------------------


def main():
    # fname = "example.txt"
    fname = "input.txt"

    m = Machine(fname)

    m.start()

    # m.debug()


##############################################################################

if __name__ == "__main__":
    main()
