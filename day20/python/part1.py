#!/usr/bin/env python3

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
        #
        self.low_pulses_cnt = 0
        self.high_pulses_cnt = 0

    def init_nodes(self) -> None:
        for k, values in self.connections.items():
            for v in values:
                node = self.get_node(v)
                if node.type == NodeType.CONJUNCTION:
                    node.inputs[k] = PulseType.LOW
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

    def press_button(self) -> None:
        src: Node = self.get_node("button")
        dest: Node = self.get_node("broadcaster")
        pulse_pool: deque[Pulse] = deque([Pulse(src, dest, PulseType.LOW)])

        while pulse_pool:  # while not empty
            pulse = pulse_pool.popleft()
            # self.debug2(pulse)
            src, dest, message = pulse.src, pulse.dest, pulse.message
            if message == PulseType.LOW:
                self.low_pulses_cnt += 1
            else:
                self.high_pulses_cnt += 1
            pulses: list[Pulse] = dest.process(message, _from=src)
            for pulse in pulses:
                pulse_pool.append(pulse)
            #
        #

    def start(self) -> None:
        for i in range(1000):
            self.press_button()
        #
        print("# low pulses counter: ", self.low_pulses_cnt)
        print("# high pulses counter:", self.high_pulses_cnt)
        print("---")
        result = self.low_pulses_cnt * self.high_pulses_cnt
        print(result)

    def debug2(self, pulse: Pulse) -> None:
        src, dest, message = pulse.src, pulse.dest, pulse.message
        msg = "-low"
        if message == PulseType.HIGH:
            msg = "-high"
        #
        print(f"{src.name} {msg}-> {dest}")

    def debug(self) -> None:
        for _, node in self.nodes.items():
            print(node)
        #
        print("---")
        for k, v in self.connections.items():
            print(f"{k} -> {v}")

    def write_dot_output(self) -> None:
        sb = [
            """
digraph D {
    // graph [concentrate=true];
    // layout=neato;
    // rankdir=LR;
    // edge [dir=none];
""".strip()
        ]
        #
        sb.append("")
        for k, values in self.connections.items():
            # print(f"{k} -> {v}")
            for v in values:
                kk = self.get_node(k).get_prefixed_name(dot=True)
                vv = self.get_node(v).get_prefixed_name(dot=True)
                sb.append(f'    "{kk}" -> "{vv}";')
        #
        sb.append("}")
        #
        text = "\n".join(sb)
        fname = "graph.dot"
        with open(fname, "w") as f:
            f.write(text)
        #
        print(f"# {fname} was created")


# ----------------------------------------------------------------------------


def main() -> None:
    # fname = "example1.txt"
    # fname = "example2.txt"
    fname = "input.txt"

    # lines = helper.read_lines("input.txt")

    g = Graph(fname)

    # g.write_dot_output()

    g.start()

    # g.debug()


##############################################################################

if __name__ == "__main__":
    main()
