from itertools import groupby
import re
from typing import List


HGT_RE = re.compile(r"^(?P<height>\d*)(?P<units>cm|in)$")
HCL_RE = re.compile(r"^#[0-9a-f]{6}$")
ECL_RE = re.compile(r"^(amb|blu|brn|gry|grn|hzl|oth)$")
PID_RE = re.compile(r"^\d{9}$")


def _validate_hgt(value: str) -> bool:
    if match := HGT_RE.match(value):
        if match.group("units") == "cm":
            return 150 <= int(match.group("height")) <= 193
        else:
            return 59 <= int(match.group("height")) <= 76

    return False


FIELD_VALIDATORS = {
    "byr": lambda value: 1920 <= int(value) <= 2002,
    "iyr": lambda value: 2010 <= int(value) <= 2020,
    "eyr": lambda value: 2020 <= int(value) <= 2030,
    "hgt": _validate_hgt,
    "hcl": lambda value: HCL_RE.match(value),
    "ecl": lambda value: ECL_RE.match(value),
    "pid": lambda value: PID_RE.match(value),
}
REQUIRED_FIELDS = FIELD_VALIDATORS.keys()


def _load_passports(path: str) -> List[dict]:
    passports = []
    with open(path) as fh:
        for is_blank, lines in groupby(fh, lambda line: line == "\n"):
            if is_blank:
                continue
            passport = {}
            for line in lines:
                for field in line.rstrip().split():
                    key, value = field.split(":")
                    passport[key] = value
            passports.append(passport)

    return passports


def _has_required_fields(passport: dict) -> bool:
    return all(required_field in passport for required_field in REQUIRED_FIELDS)


def _validate_passport(passport: dict) -> bool:
    if not _has_required_fields(passport):
        return False

    for field, value in passport.items():
        if field == "cid":
            continue

        validator = FIELD_VALIDATORS.get(field)
        if not validator(value):
            return False

    return True


# The automatic passport scanners are slow because they're having trouble detecting
# which passports have all required fields. The expected fields are as follows:

# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)

# Passport data is validated in batch files (your puzzle input). Each passport is
# represented as a sequence of key:value pairs separated by spaces or newlines.
# Passports are separated by blank lines.

# Here is an example batch file containing four passports:

# ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
# byr:1937 iyr:2017 cid:147 hgt:183cm

# iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
# hcl:#cfa07d byr:1929

# hcl:#ae17e1 iyr:2013
# eyr:2024
# ecl:brn pid:760753108 byr:1931
# hgt:179cm

# hcl:#cfa07d eyr:2025 pid:166559648
# iyr:2011 ecl:brn hgt:59in
# The first passport is valid - all eight fields are present. The second passport is
# invalid - it is missing hgt (the Height field).

# The third passport is interesting; the only missing field is cid, so it looks like
# data from North Pole Credentials, not a passport at all! Surely, nobody would mind if
# you made the system temporarily ignore missing cid fields. Treat this "passport"
# as valid.

# The fourth passport is missing two fields, cid and byr. Missing cid is fine, but
# missing any other field is not, so this passport is invalid.

# According to the above rules, your improved system would report 2 valid passports.

# Count the number of valid passports - those that have all required fields. Treat cid
# as optional. In your batch file, how many passports are valid?
def puzzle_1():
    passports = _load_passports("./day_04_data.txt")

    valid_passports = 0
    for passport in passports:
        if _has_required_fields(passport):
            valid_passports += 1

    return valid_passports


assert puzzle_1() == 260


# The line is moving more quickly now, but you overhear airport security talking about
# how passports with invalid data are getting through. Better add some data validation,
# quick!

# You can continue to ignore the cid field, but each other field has strict rules about
# what values are valid for automatic validation:

# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.

# Count the number of valid passports - those that have all required fields and valid
# values. Continue to treat cid as optional. In your batch file, how many passports are
# valid?
def puzzle_2():
    passports = _load_passports("./day_04_data.txt")

    valid_passports = 0
    for passport in passports:
        if _validate_passport(passport):
            valid_passports += 1

    return valid_passports


assert puzzle_2() == 153
