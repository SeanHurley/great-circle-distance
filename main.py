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
        rad_lat = math.radians(lat)
        rad_lon = math.radians(lon)
        r = 3959
        x = -r * math.cos(lat) * math.cos(lon)
        y = r * math.sin(lat)
        z = r * math.cos(lat) * math.sin(lon)
        coords.append((lat, lon, rad_lat, rad_lon, x, y, z))
    return coords

def __random_coord__():
    return (random.random() - .5) * 180

@timing
def haversine(conn, lat, lon, distance):
    print "Total number of results: " + str(len(conn.locations_within_haversine(100, lat, lon)))

@timing
def haversine_radians(conn, lat, lon, distance):
    print "Total number of results: " + str(len(conn.locations_within_haversine_radians(100, lat, lon)))

@timing
def straight_line(conn, lat, lon, distance):
    r = 3959
    x = -r * math.cos(lat) * math.cos(lon)
    y = r * math.sin(lat)
    z = r * math.cos(lat) * math.sin(lon)
    print "Total number of results: " + str(len(conn.locations_within_straight_line(100, x, y, z)))

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
        haversine(conn, lat, lon, 100)
        # UPDATE locations SET rad_lat = radians(lat), rad_lon = radians(lon);
        haversine_radians(conn, math.radians(lat), math.radians(lon), 100)
        # UPDATE locations SET x = -3959 * cos(rad_lat) * cos(rad_lon), y = 3959 * sin(rad_lat), z = 3959 * cos(rad_lat) * sin(rad_lon);
        straight_line(conn, math.radians(lat), math.radians(lon), 100)
        # CREATE INDEX test_index ON locations USING gist (ll_to_earth(lat, lon));
        earthdist(conn, lat, lon, 100)
