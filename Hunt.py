from random import randint


WOLF_HUNGRY = 1
WOLF = 1
SHEEP = 2
EMPTY = 0

SURROUND_MUL = 1.4


def generator(point):
    r = randint(0, 99)
    if r < 50:
        return SHEEP
    elif r >= 90:
        return WOLF
    else:
        return 0


def precalculation1(point):
    point.wolfs_count = wolfs_count(point)
    point.empty_count = empty_count(point)
    point.sheeps_count = sheeps_count(point)


def precalculation2(point):
    point.surrounded_sheeps_count = count_of_surrounded_sheeps(point)


def rule(point):
    if is_sheep(point):
        if point.wolfs_count == 0:
            return SHEEP
        elif is_surrounded_by_wolfs(point):
            return WOLF
        else:
            return EMPTY

    elif is_wolf(point):
        if point.surrounded_sheeps_count >= 1:
            return WOLF
        else:
            return point.state - 1

    else:
        if point.surrounded_sheeps_count >= 1 and point.wolfs_count >= 1:
            return WOLF_HUNGRY
        elif point.sheeps_count >= 1 and point.wolfs_count == 0:
            return SHEEP
        else:
            return EMPTY


def count_of_surrounded_sheeps(point):
    def surrounded_sheep(p):
        return is_surrounded_by_wolfs(p) and is_sheep(p)

    return ilen(filter(surrounded_sheep, point.neighbors))


def is_surrounded_by_wolfs(point):
    empty = point.empty_count
    wolfs = point.wolfs_count
    return empty * SURROUND_MUL <= wolfs


def empty_count(point):
    return ilen(filter(lambda x: x.state == EMPTY, point.neighbors))


def wolfs_count(point):
    return ilen(filter(is_wolf, point.neighbors))


def sheeps_count(point):
    return ilen(filter(is_sheep, point.neighbors))


def ilen(iterable):
    return sum(1 for _ in iterable)


def is_sheep(point):
    return point.state == SHEEP


def is_wolf(point):
    return WOLF_HUNGRY <= point.state <= WOLF
