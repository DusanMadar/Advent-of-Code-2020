from functools import reduce
from typing import List


def _load_map(path: str) -> List[str]:
    map_ = []
    with open(path) as fh:
        for line in fh:
            map_.append(line.rstrip())

    return map_


def _count_trees(map_: List[str], right: int, down: int) -> int:
    tree_count = 0
    column = 0
    for line in map_[::down]:
        if column == len(line):
            column = 0
        elif column > len(line):
            column = column - len(line)
        if line[column] == "#":
            tree_count += 1
        column += right

    return tree_count


# You start on the open square (.) in the top-left corner and need to reach the bottom
# (below the bottom-most row on your map).

# The toboggan can only follow a few specific slopes (you opted for a cheaper model
# that prefers rational numbers); start by counting all the trees you would encounter
# for the slope right 3, down 1:

# From your starting position at the top-left, check the position that is right 3 and
# down 1. Then, check the position that is right 3 and down 1 from there, and so on
# until you go past the bottom of the map.

# The locations you'd check in the above example are marked here with O where there
# was an open square and X where there was a tree:

# ..##.........##.........##.........##.........##.........##.......  --->
# #..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
# .#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
# ..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
# .#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
# ..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
# .#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
# .#........#.#........X.#........#.#........#.#........#.#........#
# #.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
# #...##....##...##....##...#X....##...##....##...##....##...##....#
# .#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
# In this example, traversing the map using this slope would cause you to encounter
# 7 trees.

# Starting at the top-left corner of your map and following a slope of right 3 and down
# 1, how many trees would you encounter?
def puzzle_1():
    map_ = _load_map("./day_03_data.txt")
    return _count_trees(map_, 3, 1)


assert puzzle_1() == 195


# Time to check the rest of the slopes - you need to minimize the probability of a
# sudden arboreal stop, after all.

# Determine the number of trees you would encounter if, for each of the following
# slopes, you start at the top-left corner and traverse the map all the way to the
# bottom:

# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.
# In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s) respectively;
# multiplied together, these produce the answer 336.

# What do you get if you multiply together the number of trees encountered on each of
# the listed slopes?
def puzzle_2():
    map_ = _load_map("./day_03_data.txt")

    tree_counts = []
    for right, down in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
        tree_counts.append(_count_trees(map_, right, down))

    return reduce(lambda x, y: x * y, tree_counts)


assert puzzle_2() == 3772314000
