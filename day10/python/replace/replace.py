#!/usr/bin/env python3

import sys

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
