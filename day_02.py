# Each line gives the password policy and then the password. The password policy
# indicates the lowest and highest number of times a given letter must appear for the
# password to be valid. For example, 1-3 a means that the password must contain a at
# least 1 time and at most 3 times.

# In the above example, 2 passwords are valid. The middle password, cdefg, is not; it
# contains no instances of b, but needs at least 1. The first and third passwords are
# valid: they contain one a or nine c, both within the limits of their respective policies.

# How many passwords are valid according to their policies?
def puzzle_1():
    with open("./day_02_data.txt") as fh:
        passwords = fh.readlines()

    valid_passwords = 0
    for password in passwords:
        policy, password = password.split(": ")
        limits, letter = policy.split(" ")
        limits = tuple(int(l) for l in limits.split("-"))

        if limits[0] <= password.count(letter) <= limits[1]:
            valid_passwords += 1

    return valid_passwords


assert puzzle_1() == 416


# The shopkeeper suddenly realizes that he just accidentally explained the password
# policy rules from his old job at the sled rental place down the street! The Official
# Toboggan Corporate Policy actually works a little differently.

# Each policy actually describes two positions in the password, where 1 means the first
# character, 2 means the second character, and so on. (Be careful; Toboggan Corporate
# Policies have no concept of "index zero"!) Exactly one of these positions must contain
# the given letter. Other occurrences of the letter are irrelevant for the purposes of
# policy enforcement.

# Given the same example list from above:

# 1-3 a: abcde is valid: position 1 contains a and position 3 does not.
# 1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
# 2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.
# How many passwords are valid according to the new interpretation of the policies?
def puzzle_2():
    with open("./day_02_data.txt") as fh:
        passwords = fh.readlines()

    valid_passwords = 0
    for password in passwords:
        policy, password = password.split(": ")
        positions, letter = policy.split(" ")
        positions = tuple(int(p) - 1 for p in positions.split("-"))

        position_one = password[positions[0]] == letter
        position_two = password[positions[1]] == letter
        if sum((position_one, position_two)) == 1:
            valid_passwords += 1

    return valid_passwords


assert puzzle_2() == 688
