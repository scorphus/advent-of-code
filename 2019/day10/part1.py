import sys
from dataclasses import dataclass, field
from math import atan, degrees
from typing import Set


@dataclass
class Asteroid:
    row: int
    col: int
    sight_lines: Set[float] = field(default_factory=set)

    def add_sight_line(self, other):
        if other.col == self.col:
            tangent = float("inf") * (self.row - other.row)
        else:
            tangent = (self.row - other.row) / (other.col - self.col)
        angle = degrees(atan(tangent))
        if other.col < self.col:
            angle -= 180
        self.sight_lines.add(angle)

    def add_sight_lines(self, belt):
        for other in belt:
            if other == self:
                continue
            self.add_sight_line(other)
        return len(self.sight_lines)


def load_belt():
    with open(sys.argv[1]) as f:
        return [
            Asteroid(row, col)
            for row, line in enumerate(f.readlines())
            for col, c in enumerate(line.rstrip())
            if c == "#"
        ]


def main():
    belt = load_belt()
    print(max(asteroid.add_sight_lines(belt) for asteroid in belt))


if __name__ == "__main__":
    main()
