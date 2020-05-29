import sys
from dataclasses import dataclass, field
from math import atan, degrees, sqrt
from typing import Dict


@dataclass
class Asteroid:
    row: int
    col: int
    neighbors: Dict[float, tuple] = field(default_factory=dict)

    def distance_from(self, other):
        return sqrt(pow(other.row - self.row, 2) + pow(other.col - self.col, 2))

    def add_neighbor(self, other):
        if other.col == self.col:
            tangent = float("inf") * (self.row - other.row)
        else:
            tangent = (self.row - other.row) / (other.col - self.col)
        angle = degrees(atan(tangent))
        if other.col >= self.col:
            angle = 90 - angle
        else:
            angle = 270 - angle
        distance = self.distance_from(other)
        if angle in self.neighbors and distance > self.neighbors[angle][0]:
            return
        self.neighbors[angle] = (distance, other)

    def add_neighbors(self, belt):
        for other in belt:
            if other == self:
                continue
            self.add_neighbor(other)
        return len(self.neighbors)

    def vaporize_asteroids(self, nth):
        neighbors = sorted(self.neighbors)
        count = 0
        while True:
            last_count = count
            for i, key in enumerate(neighbors):
                if key is None:
                    continue
                count += 1
                if count == nth:
                    return self.neighbors[key][1]
                if key in self.neighbors[key][1].neighbors:
                    self.neighbors[key] = self.neighbors[key][1].neighbors[key]
                else:
                    neighbors[i] = None
            if count == last_count:
                break


def load_belt():
    with open(sys.argv[1]) as f:
        return [
            Asteroid(row, col)
            for row, line in enumerate(f.readlines())
            for col, c in enumerate(line.rstrip())
            if c == "#"
        ]


def find_best_location(belt):
    max_neighbors = 0
    for asteroid in belt:
        num_neighbors = asteroid.add_neighbors(belt)
        if num_neighbors > max_neighbors:
            best_asteroid, max_neighbors = asteroid, num_neighbors
    return best_asteroid


def main():
    belt = load_belt()
    best_asteroid = find_best_location(belt)
    the_one_asteroid = best_asteroid.vaporize_asteroids(200)
    if the_one_asteroid:
        print(the_one_asteroid.col * 100 + the_one_asteroid.row)
    else:
        print("Seems like all asteroids were vaporized!")


if __name__ == "__main__":
    main()
