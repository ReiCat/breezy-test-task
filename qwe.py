# def create_set():
#     my_set = {1, 2, 3, 4, 5}
#     print('create_set', my_set)


# def add_element():
#     my_set = {1, 2, 3, 4, 5}
#     my_set.add(6)
#     print('add_element', my_set)


# def remove_element():
#     my_set = {1, 2, 3, 4, 5}
#     my_set.remove(3)
#     print('remove_element', my_set)


# def clear_set():
#     my_set = {1, 2, 3, 4, 5}
#     my_set.clear()
#     print('clear_set', my_set)


def set_union():
    set1 = {1, 2, 3}
    set2 = {4, 5, 6}
    my_set = set1.union(set2)
    print('set_union', my_set)


def set_intersection():
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    my_set = set1.intersection(set2)
    print('set_intersection', my_set)


def set_difference():
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    my_set = set1.difference(set2)
    print('set_difference', my_set)


def set_symmetric_difference():
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    my_set = set1.symmetric_difference(set2)
    print('set_symmetric_difference', my_set)


def set_subset():
    set1 = {1, 2, 3, 4, 5}
    set2 = {2, 3, 4}
    subset = set2.issubset(set1)
    print('set_subset', subset)


def set_superset():
    set1 = {1, 2, 3, 4, 5}
    set2 = {2, 3, 4}
    superset = set1.issuperset(set2)
    print('set_superset', superset)


if __name__ == '__main__':
    # create_set()
    # add_element()
    # remove_element()
    # clear_set()
    set_union()
    set_intersection()
    set_difference()
    set_symmetric_difference()
    set_subset()
    set_superset()
