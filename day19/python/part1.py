#!/usr/bin/env python3

from enum import Enum, auto

import helper

# ----------------------------------------------------------------------------


class Status(Enum):
    ACCEPT = auto()
    REJECT = auto()


# ----------------------------------------------------------------------------


class Workflow:
    def __init__(self, line: str) -> None:
        self._id, rest = line.split("{")
        rest = rest.rstrip("}")
        self.rules = rest.split(",")

    def apply(self, part: dict) -> str:
        for rule in self.rules:
            if ":" in rule:
                condition, action = rule.split(":")
                if "<" in condition:
                    var, value = condition.split("<")
                    if part[var] < int(value):
                        return action
                    #
                elif ">" in condition:
                    var, value = condition.split(">")
                    if part[var] > int(value):
                        return action
                    #
                else:
                    assert False, "We should never get here"
            else:
                return rule
            #
        #
        assert False, "We should never get here"

    def __str__(self) -> str:
        d = {
            "id": self._id,
            "rules": self.rules,
        }
        return str(d)


# ----------------------------------------------------------------------------


class Machine:
    def __init__(self, fname: str) -> None:
        content = helper.read(fname)
        first, second = content.split("\n\n")
        self.workflows: dict[str, Workflow] = self.parse_workflows(first)
        self.parts: list[dict] = self.parse_parts(second)

    def parse_workflows(self, text: str) -> dict[str, Workflow]:
        result: dict[str, Workflow] = {}
        lines = text.splitlines()
        for line in lines:
            wf = Workflow(line)
            result[wf._id] = wf
        #
        return result

    def parse_parts(self, text: str) -> list[dict]:
        result: list[dict] = []
        lines = text.splitlines()
        for line in lines:
            line = line.strip("{}")
            d = {}
            parts = line.split(",")
            for p in parts:
                l, r = p.split("=")
                d[l] = int(r)
            #
            result.append(d)
        #
        return result

    def process(self, part: dict) -> Status:
        wf = self.workflows["in"]

        while True:
            result: str = wf.apply(part)
            if result == "A":
                return Status.ACCEPT
            elif result == "R":
                return Status.REJECT
            else:
                wf = self.workflows[result]
            #
        #

    def start(self) -> None:
        accepted: list[dict] = []

        for p in self.parts:
            if self.process(p) == Status.ACCEPT:
                accepted.append(p)
            #
        #
        total = 0
        for a in accepted:
            total += sum(a.values())
        #
        print(total)


# ----------------------------------------------------------------------------


def main():
    # fname = "example.txt"
    fname = "input.txt"

    m = Machine(fname)

    m.start()


##############################################################################

if __name__ == "__main__":
    main()
