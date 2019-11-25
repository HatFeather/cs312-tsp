import math


def compute_sqr_dist(city_a, city_b):
    x = city_b._x - city_a._x
    y = city_b._y - city_a._y
    return math.sqrt(x * x + y * y)


def compute_dist(city_a, city_b):
    sqr_dist = compute_sqr_dist(city_a, city_b)
    return math.sqrt(sqr_dist)
