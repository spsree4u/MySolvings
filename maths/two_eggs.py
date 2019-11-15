

"""
You are given two eggs, and access to a 100-storey building.
Both eggs are identical. The aim is to find out the highest floor
from which an egg will not break when dropped out of a window from that floor.
If an egg is dropped and does not break, it is undamaged and can be
dropped again. However, once an egg is broken, that’s it for that egg.

What strategy should you adopt to minimize the number egg drops it takes to
find the solution?.
"""


def drop_egg(floor):
    return 0 if floor <= 101 else 1


def second_egg(current_floor):
    while drop_egg(current_floor):
        current_floor -= 1
    return current_floor


def first_egg():
    current_floor = 14
    next_floor_jump = current_floor
    while current_floor <= 100:
        next_floor_jump -= 1
        is_broken = drop_egg(current_floor)
        if is_broken:
            return second_egg(current_floor)
        elif current_floor == 100:
            return current_floor
        current_floor = current_floor + next_floor_jump
        if current_floor > 100:
            current_floor = 100


print(first_egg())
