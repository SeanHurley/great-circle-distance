from psql import Psql
import math
import random
import time

def populate():
    coords = []
    for x in range(0,1000000):
        coords.append((__random_coord__(), __random_coord__()))
    return coords

def __random_coord__():
    return (random.random() - .5) * 180

if __name__ == "__main__":
    coords = populate()
    connection = Psql()
    connection.insert_locations(coords)
