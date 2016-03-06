from itertools import tee, chain


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def pairwise_looped(iterable):
    a, b = tee(iterable)
    b_first = next(b, None)
    b = chain(b, [b_first])
    return zip(a, b)


if __name__ == '__main__':
    for a, b in pairwise_looped([1, 2, 3, 4, 5]):
        print(a, b, a+b)
