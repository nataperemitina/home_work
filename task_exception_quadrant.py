def get_quadrant_number(x, y):
    if not x or not y:
        raise ValueError()

    if x > 0:
        if y > 0:
            return 1
        else:
            return 4
    elif y > 0:
        return 2
    else:
        return 3


