from math import ceil, floor
from typing import List, Tuple


def _load_boarding_passes(path: str) -> List[str]:
    with open(path) as fh:
        return fh.readlines()


def _resolve_range(is_lower_half: bool, rows_range: Tuple[int, int]) -> Tuple[int, int]:
    middle = (rows_range[1] - rows_range[0]) / 2

    if is_lower_half:
        lower = rows_range[0]
        upper = rows_range[0] + floor(middle)
    else:
        lower = rows_range[0] + ceil(middle)
        upper = rows_range[1]

    return lower, upper


def _decode_seat_id_naive(boarding_pass: str) -> int:
    rows_range = (0, 127)
    for direction in list(boarding_pass[:7]):
        rows_range = _resolve_range(direction == "F", rows_range)

    columns_range = (0, 7)
    for direction in list(boarding_pass[7:]):
        columns_range = _resolve_range(direction == "L", columns_range)

    return rows_range[0] * 8 + columns_range[0]


def _decode_seat_id_binary(boarding_pass: str) -> int:
    boarding_pass = boarding_pass.replace("F", "0").replace("B", "1")
    boarding_pass = boarding_pass.replace("L", "0").replace("R", "1")
    return int(boarding_pass[:7], 2) * 8 + int(boarding_pass[7:], 2)


# You board your plane only to discover a new problem: you dropped your boarding pass!
# You aren't sure which seat is yours, and all of the flight attendants are busy with
# the flood of people that suddenly made it through passport control.

# You write a quick program to use your phone's camera to scan all of the nearby
# boarding passes (your puzzle input); perhaps you can find your seat through process
# of elimination.

# Instead of zones or groups, this airline uses binary space partitioning to seat
# people. A seat might be specified like FBFBBFFRLR, where F means "front", B means
# "back", L means "left", and R means "right".

# The first 7 characters will either be F or B; these specify exactly one of the 128
# rows on the plane (numbered 0 through 127). Each letter tells you which half of a
# region the given seat is in. Start with the whole list of rows; the first letter
# indicates whether the seat is in the front (0 through 63) or the back (64 through
# 127). The next letter indicates which half of that region the seat is in, and so on
# until you're left with exactly one row.

# For example, consider just the first seven characters of FBFBBFFRLR:

# Start by considering the whole range, rows 0 through 127.
# F means to take the lower half, keeping rows 0 through 63.
# B means to take the upper half, keeping rows 32 through 63.
# F means to take the lower half, keeping rows 32 through 47.
# B means to take the upper half, keeping rows 40 through 47.
# B keeps rows 44 through 47.
# F keeps rows 44 through 45.
# The final F keeps the lower of the two, row 44.
# The last three characters will be either L or R; these specify exactly one of the
# 8 columns of seats on the plane (numbered 0 through 7). The same process as above
# proceeds again, this time with only three steps. L means to keep the lower half,
# while R means to keep the upper half.

# For example, consider just the last 3 characters of FBFBBFFRLR:

# Start by considering the whole range, columns 0 through 7.
# R means to take the upper half, keeping columns 4 through 7.
# L means to take the lower half, keeping columns 4 through 5.
# The final R keeps the upper of the two, column 5.
# So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

# Every seat also has a unique seat ID: multiply the row by 8, then add the column. In
# this example, the seat has ID 44 * 8 + 5 = 357.
def puzzle_1():
    boarding_passes = _load_boarding_passes("./day_05_data.txt")
    return max(_decode_seat_id_binary(bp.strip()) for bp in boarding_passes)


assert puzzle_1() == 896


# It's a completely full flight, so your seat should be the only missing boarding pass
# in your list. However, there's a catch: some of the seats at the very front and back
# of the plane don't exist on this aircraft, so they'll be missing from your list as
# well.

# Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from
# yours will be in your list.
def puzzle_2():
    boarding_passes = _load_boarding_passes("./day_05_data.txt")
    seat_ids = set(_decode_seat_id_binary(bp.strip()) for bp in boarding_passes)
    return tuple(set(range(min(seat_ids), max(seat_ids) + 1)).difference(seat_ids))[0]


assert puzzle_2() == 659
