#!/usr/bin/env rdmd

import std.algorithm;
import std.array;
import std.ascii;
import std.conv;
import std.file;
import std.range;
import std.regex;
import std.stdio;
import std.string;

immutable DIGITS = [
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9,
];

string rev(const string s) pure
{
    return s.retro.to!string;
}

int text2number(const string s) pure
{
    // dfmt off
    if (s.length == 1) {
        return s.to!int;
    }
    // else
    return DIGITS[s];
    // dfmt on
}

int get_number(const string s)
{
    auto m = matchFirst(s, regex(`1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine`));
    assert(!m.empty);
    int first = text2number(m.hit);
    //
    m = matchFirst(rev(s), regex(`1|2|3|4|5|6|7|8|9|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin`));
    assert(!m.empty);
    int last = text2number(rev(m.hit));

    return first * 10 + last;
}

void main()
{
    // const fname = "example2.txt";
    const fname = "input.txt";

    const lines = readText(fname).splitLines;
    const numbers = lines.map!(line => get_number(line)).array;

    // writeln(lines);
    // writeln(numbers);
    writeln(numbers.sum);
}
