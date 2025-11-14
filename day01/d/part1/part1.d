#!/usr/bin/env rdmd

import std.stdio;
import std.file;
import std.algorithm;
import std.string;
import std.array;
import std.ascii;

int get_number(const string s) pure
{
    char first = '-'; // not yet set
    char last = '-'; // not yet set

    foreach (c; s)
    {
        if (c.isDigit)
        {
            // dfmt off
            if (first == '-') {
                first = last = c;
            } else {
                last = c;
            }
            // dfmt on
        }
    }
    return (first - '0') * 10 + (last - '0');
}

void main()
{
    // const fname = "example1.txt";
    const fname = "input.txt";

    const lines = readText(fname).splitLines;
    const numbers = lines.map!(line => get_number(line)).array;

    // writeln(lines);
    writeln(numbers.sum);
}
