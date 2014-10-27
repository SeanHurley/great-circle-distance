from psql import Psql
import math
import random
import time

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

def populate(num_records):
    coords = []
    for x in range(0,num_records):
        lat = __random_coord__()
        lon = __random_coord__()
        coords.append((lat, lon))
    return coords

def __random_coord__():
    return (random.random() - .5) * 180

@timing
def earthdist(conn, lat, lon, distance):
    print "Total number of results: " + str(len(conn.locations_within_earthdist(100, lat, lon)))

if __name__ == "__main__":
    connection = Psql()
    connection.truncate_locations()

    total = 0
    for i in range(1,4):
        to_add = 10**i * 1000 - total
        coords = populate(to_add)
        connection.insert_locations(coords)
        total = 10**i * 1000

        conn = Psql()
        lat = 41.89195
        lon = -87.628533

        print
        print
        print "With " + str(total) + " records:"

        #https://gist.github.com/norman/1535879
        # CREATE INDEX test_index ON locations USING gist (ll_to_earth(lat, lon));
        earthdist(conn, lat, lon, 100)
