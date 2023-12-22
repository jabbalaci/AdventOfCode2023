#!/usr/bin/env python3

"""
First I tried the naive approach but I quickly realized
that it would never finish.

So I used some help from here:
https://old.reddit.com/r/adventofcode/comments/18ohnwh/2023_day_20_part_2_understanding_why_it_works/
"""

import math
from collections import deque
from enum import Enum, auto

import helper

# ----------------------------------------------------------------------------


class NodeType(Enum):
    NONAME = auto()
    FLIP_FLOP = auto()
    CONJUNCTION = auto()


class PulseType(Enum):
    LOW = auto()
    HIGH = auto()


# ----------------------------------------------------------------------------


class Node:
    def __init__(self, name: str, _type: NodeType, parent: "Graph") -> None:
        self.name: str = name
        self.type: NodeType = _type
        self.parent = parent
        # if it's a flip-flop node
        self.status = 0  # 0: off, 1: on
        # if it's a conjunction node
        self.inputs: dict[str, PulseType] = {}

    def get_prefixed_name(self, dot=False) -> str:
        prefix = ""
        if self.type == NodeType.FLIP_FLOP:
            prefix = "%"
        elif self.type == NodeType.CONJUNCTION:
            prefix = "&"
        #
        if dot and prefix:
            prefix = "\\" + prefix
        #
        return f"{prefix}{self.name}"

    def process(self, message: PulseType, _from: "Node") -> list["Pulse"]:
        result: list["Pulse"] = []
        if self.name == "broadcaster":
            assert _from.name == "button"
            assert message == PulseType.LOW
            for v in self.parent.connections["broadcaster"]:
                result.append(Pulse(self, self.parent.get_node(v), PulseType.LOW))
            #
        #
        if self.type == NodeType.FLIP_FLOP:
            if message == PulseType.HIGH:
                pass  # nothing happens
            else:
                self.status = 1 - self.status  # flip status
                to_send = PulseType.LOW  # if new status is off
                if self.status == 1:  # if new status is on
                    to_send = PulseType.HIGH
                #
                for v in self.parent.connections[self.name]:
                    result.append(Pulse(self, self.parent.get_node(v), to_send))
                #
            #
        #
        if self.type == NodeType.CONJUNCTION:
            self.inputs[_from.name] = message
            to_send = PulseType.HIGH
            if all(v == PulseType.HIGH for v in self.inputs.values()):
                to_send = PulseType.LOW
            #
            for v in self.parent.connections[self.name]:
                result.append(Pulse(self, self.parent.get_node(v), to_send))
            #
        #
        return result

    def __str__(self) -> str:
        return self.get_prefixed_name()


# ----------------------------------------------------------------------------


class Pulse:
    def __init__(self, src: Node, dest: Node, message: PulseType) -> None:
        self.src = src
        self.dest = dest
        self.message = message


# ----------------------------------------------------------------------------


class Graph:
    def __init__(self, fname: str) -> None:
        self.lines = helper.read_lines(fname)
        self.nodes = {
            "button": Node("button", NodeType.NONAME, self),
        }
        self.connections: dict[str, list[str]] = {}
        self.connections["button"] = ["broadcaster"]
        self.parse_input()
        self.init_nodes()

    def init_nodes(self) -> None:
        for k, values in self.connections.items():
            for v in values:
                node = self.get_node(v)
                if node.type == NodeType.CONJUNCTION:
                    node.inputs[k] = PulseType.LOW
                elif node.type == NodeType.FLIP_FLOP:
                    node.status = 0  # off
                #
            #
        #

    def get_node(self, name: str) -> Node:
        return self.nodes[name]

    def parse_input(self) -> None:
        d = self.nodes

        for line in self.lines:
            left, right = line.split(" -> ")
            # process left side
            _type = NodeType.NONAME
            if left.startswith("%"):
                _type = NodeType.FLIP_FLOP
            elif left.startswith("&"):
                _type = NodeType.CONJUNCTION
            left_name = left.lstrip("%&")
            if left_name not in d:
                d[left_name] = Node(left_name, _type, self)
            else:
                # update type if necessary
                node = d[left_name]
                if node.type == NodeType.NONAME and _type != NodeType.NONAME:
                    node.type = _type
                #
            #
            # process right side
            right_parts = right.split(", ")
            for right_name in right_parts:
                if right_name not in d:
                    d[right_name] = Node(right_name, NodeType.NONAME, self)
                #
                if left_name not in self.connections:
                    self.connections[left_name] = []
                #
                self.connections[left_name].append(right_name)
            #
        #

    def press_button(self, name: str) -> bool:
        src: Node = self.get_node("button")
        dest: Node = self.get_node("broadcaster")
        pulse_pool: deque[Pulse] = deque([Pulse(src, dest, PulseType.LOW)])

        stop = False
        while pulse_pool:  # while not empty
            pulse = pulse_pool.popleft()
            # self.debug2(pulse)
            src, dest, message = pulse.src, pulse.dest, pulse.message
            if (src.name == name) and (message == PulseType.HIGH):
                stop = True
                return stop
            #
            pulses: list[Pulse] = dest.process(message, _from=src)
            for pulse in pulses:
                pulse_pool.append(pulse)
            #
        #
        return stop

    def who_points_to(self, dest: str) -> list[str]:
        return [k for k, values in self.connections.items() if dest in values]

    def start(self) -> None:
        nodes: list[str] = self.who_points_to("rx")
        assert len(nodes) == 1
        points_to_rx: str = nodes[0]
        nodes = self.who_points_to(points_to_rx)
        print(nodes)

        collect: list[int] = []
        for node in nodes:
            self.init_nodes()
            cnt = 0
            while True:
                stop = self.press_button(node)
                cnt += 1
                if stop:
                    break
                #
            #
            collect.append(cnt)
        #
        print(collect)
        print("---")
        result = math.lcm(*collect)
        print(result)


# ----------------------------------------------------------------------------


def main() -> None:
    fname = "input.txt"

    g = Graph(fname)
    g.start()


##############################################################################

if __name__ == "__main__":
    main()
