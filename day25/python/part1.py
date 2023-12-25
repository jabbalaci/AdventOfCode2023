#!/usr/bin/env python3

"""
To figure out what 3 connections to cut, I used some visualization.
Once `connections_input.jpg` was ready, it was easy to see what
connections had to be cut.
"""

from collections import deque
from pprint import pprint

import helper


class Graph:
    def __init__(self, fname: str, connections_to_cut: list[str]) -> None:
        self.lines: list[str] = helper.read_lines(fname)
        self.d: dict[str, list[str]] = self.parse()
        self.remove_self_references()
        self.make_undirected()
        self.remove_duplicates()
        self.group1_node, self.group2_node = connections_to_cut[0].split("/")
        self.cut_connections(connections_to_cut)

    def cut_connections(self, connections_to_cut: list[str]) -> None:
        d = self.d
        for conn in connections_to_cut:
            l, r = conn.split("/")
            if r in d[l]:
                d[l].remove(r)
            #
            if l in d[r]:
                d[r].remove(l)
            #
        #

    def remove_duplicates(self) -> None:
        for k, values in self.d.items():
            self.d[k] = list(set(values))
        #

    def make_undirected(self) -> None:
        new: dict[str, list[str]] = {}
        for k, values in self.d.items():
            for v in values:
                if k not in new:
                    new[k] = []
                new[k].append(v)
                if v not in new:
                    new[v] = []
                new[v].append(k)
            #
        #
        self.d = new

    def remove_self_references(self) -> None:
        for k, values in self.d.items():
            to_remove = []
            for v in values:
                if v == k:
                    to_remove.append(v)
                #
            #
            for e in to_remove:
                values.remove(e)
            #
        #

    def parse(self) -> dict[str, list[str]]:
        d: dict[str, list[str]] = {}
        #
        for line in self.lines:
            left, r = line.split(":")
            right = r.split()
            d[left] = right
        #
        return d

    def create_dot(self) -> None:
        sb: list[str] = [
            """
digraph D {
    // graph [concentrate=true];
    layout=neato;
    // rankdir=LR;
    edge [dir=none];
""".strip()
        ]
        sb.append("")
        #
        for k, v in self.d.items():
            value = str(v).replace("[", "{").replace("]", "}").replace(",", "").replace("'", "")
            sb.append(f"    {k} -> {value};")
        #
        sb.append("}")

        with open("graph.dot", "w") as f:
            f.write("\n".join(sb))
        #
        print("# graph.dot was created")

    def traverse(self, start_node: str) -> int:
        d = self.d
        if start_node not in d:
            raise Exception(f"start node '{start_node}' not found")
        # else
        visited: list[str] = []
        visible: deque[str] = deque([start_node])

        while visible:  # while not empty
            curr = visible.popleft()
            can_be_seen = d[curr]
            for e in can_be_seen:
                if (e not in visible) and (e not in visited):
                    visible.append(e)
                #
            #
            visited.append(curr)
            #
            # print(visited)
            # print(visible)
            # print("---")
            # input()
        #
        return len(visited)

    def start(self) -> None:
        size1 = self.traverse(self.group1_node)
        size2 = self.traverse(self.group2_node)
        #
        print(size1)
        print(size2)
        print("---")
        result = size1 * size2
        print(result)

    def debug(self) -> None:
        pprint(self.d)


def main() -> None:
    # g = Graph("example.txt", ["hfx/pzl", "bvb/cmg", "nvd/jqt"])
    g = Graph("input.txt", ["hcd/cnr", "fqr/bqp", "zsp/fhv"])

    g.start()

    # g.create_dot()

    # g.debug()


##############################################################################

if __name__ == "__main__":
    main()
