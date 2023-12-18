#!/usr/bin/env python3


def area(p):
    return 0.5 * abs(sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in segments(p)))


def segments(p):
    return zip(p, p[1:] + [p[0]])


def my_area(vertices):
    N = len(vertices)
    area = 0.0
    for i in range(N - 1):
        j = (i + 1) % N
        area = area + vertices[i][0] * vertices[j][1]
        area = area - vertices[i][1] * vertices[j][0]
    #
    return abs(area) / 2


def main():
    points = [
        (0, 0),
        (0, 6),  # 6
        (5, 6),  # 5
        (5, 4),  # 2
        (7, 4),  # 2
        (7, 6),  # 2
        (9, 6),  # 2
        (9, 1),  # 5
        (7, 1),  # 2
        (7, 0),  # 1
        (5, 0),  # 2
        (5, 2),  # 2
        (2, 2),  # 3
        (2, 0),  # 2
    ]
    # points = [(0, 0), (5, 0), (5, 5), (0, 5)]
    # points = [(0, 0), (0, 1), (1, 1), (1, 0)]
    # points = [(1 - 0.5, 1 - 0.5), (1 - 0.5, 2 + 0.5), (2 + 0.5, 2 + 0.5), (2 + 0.5, 1 - 0.5)]
    result = area(points)
    # result = my_area(points)
    print(result)


##############################################################################

if __name__ == "__main__":
    main()
