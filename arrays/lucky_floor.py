"""
For a given number of floors, find the top floor number (lucky floor)
in a building in such a way that there shouldn't be floor number contains
4 or 13 (ex: [1,2,3,5,..,10,11,12,15,16,...23,25,...39,50,..,103,..112,115,..])
ex: 14 floor building
Normal floors will be : [1,2,3,4,5,6,7,8,9,10,11,12,13,14], top_floor = 14
Our building floors are: [1,2,3,5,6,7,8,9,10,11,12,15,16,17], top_floor = 16

"""


def get_lucky_floor_number(n):
    lucky = n
    for i in range(1, n+1):
        if str(i).__contains__('4') or str(i).__contains__('13'):
            lucky += 1
    print(lucky)
    return lucky


get_lucky_floor_number(1)
get_lucky_floor_number(11)
get_lucky_floor_number(14)


def get_lucky_floor_number2(n):
    """
    Implementation is not completed
    :param n:
    :return:
    """
    floors = []
    for i in range(1, n+1):
        while i > 0:
            if i % 100 == 13:
                floors.append(i)
                break
            if i % 10 == 4:
                floors.append(i)
                break
            else:
                i /= 10

    # print(floors)
    if floors:
        print(n + len(floors))
        return n + len(floors)
    else:
        print(n)
        return n


# get_lucky_floor_number2(3)
# get_lucky_floor_number2(55)
# get_lucky_floor_number2(14)
