#!/usr/bin/env python3

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import helper

d = {
    "F": "┌",
    "7": "┐",
    "L": "└",
    "J": "┘",
}


def main():
    fname = sys.argv[1]
    content = helper.read(fname)
    for k, v in d.items():
        content = content.replace(k, v)
    #
    print(content)


##############################################################################

if __name__ == "__main__":
    main()
