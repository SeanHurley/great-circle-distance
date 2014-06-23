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

def populate():
    coords = []
    for x in range(0,1000000):
        coords.append((__random_coord__(), __random_coord__()))
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

if __name__ == "__main__":
    #coords = populate()
    #connection = Psql()
    #connection.insert_locations(coords)

    conn = Psql()
    lat = 41.89195
    lon = -87.628533

    haversine(conn, lat, lon, 100)
    # UPDATE locations SET rad_lat = radians(lat), rad_lon = radians(lon);
    haversine_radians(conn, math.radians(lat), math.radians(lon), 100)
    # UPDATE locations SET x = -3959 * cos(rad_lat) * cos(rad_lon), y = 3959 * sin(rad_lat), z = 3959 * cos(rad_lat) * sin(rad_lon);
    straight_line(conn, math.radians(lat), math.radians(lon), 100)
