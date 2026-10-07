import math


def distance(p1, p2):

    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


def collision_risk(pos1, pos2, threshold=100):

    if pos1 is None or pos2 is None:
        return False

    return distance(pos1, pos2) < threshold