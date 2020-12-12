from typing import List


def _load_expenses(path: str, threshold: int) -> List[int]:
    expenses = []
    with open(path) as fh:
        for line in fh:
            expense = int(line.rstrip())
            if expense < threshold:
                expenses.append(expense)

    return expenses


# Before you leave, the Elves in accounting just need you to fix your expense report
# (your puzzle input); apparently, something isn't quite adding up.
#
# Specifically, they need you to find the two entries that sum to 2020 and then multiply
# those two numbers together.
def puzzle_1():
    expenses = sorted(_load_expenses("./day_01_data.txt", 2020))
    min_expense = expenses[0]
    max_expense = expenses[-1]

    for index, expense in enumerate(expenses):
        diff = 2020 - expense
        if min_expense > diff > max_expense:
            continue
        if diff in expenses[index + 1 :]:
            return expense * diff


assert puzzle_1() == 1020099


# The Elves in accounting are thankful for your help; one of them even offers you a
# starfish coin they had left over from a past vacation. They offer you a second one if
# you can find three numbers in your expense report that meet the same criteria.
def puzzle_2():
    expenses = sorted(_load_expenses("./day_01_data.txt", 2020))
    min_expense = expenses[0]
    max_expense = expenses[-1]

    for index, expense in enumerate(expenses):
        for next_expense in expenses[index + 1 :]:
            diff = 2020 - expense - next_expense
            if min_expense > diff > max_expense:
                break
            if diff in expenses[index + 2 :]:
                return expense * next_expense * diff


assert puzzle_2() == 49214880
