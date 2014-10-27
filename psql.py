import psycopg2
import sys
import re
import datetime

r = 3959
class Psql:
    def __init__(self):
        self.con = psycopg2.connect(database='geo', user='hurley', host="/tmp")
        self.cur = self.con.cursor()

    def truncate_locations(self):
        self.cur.execute("TRUNCATE TABLE locations")
        self.con.commit()

    def insert_locations(self, coords):
        args_str = ','.join(self.cur.mogrify("(DEFAULT,%s,%s)", x) for x in coords)
        self.cur.execute("INSERT INTO locations VALUES " + args_str)
        self.con.commit()

    def locations_within_haversine(self, distance, lat, lon):
        query = """
        SELECT *
        FROM locations loc
        WHERE
            2 * %(r)s * abs(
                asin(
                    sqrt(
                        pow(sin((radians(%(lat)s) - radians(loc.lat)) / 2), 2) +
                        cos(radians(%(lat)s)) * cos(radians(loc.lat)) * pow(sin((radians(%(lon)s) - radians(loc.lon)) / 2), 2)
                    )
                )
            )
            <= %(distance)s
        """ % {"r": r, "distance": distance, "lat": lat, "lon": lon}
        return self.__execute__(query)

    def locations_within_haversine_radians(self, distance, lat, lon):
        query = """
        SELECT *
        FROM locations loc
        WHERE
            2 * %(r)s * abs(
                asin(
                    sqrt(
                        pow((sin(%(lat)s - loc.rad_lat) / 2), 2) +
                        cos(%(lat)s) * cos(loc.rad_lat) * pow((sin(%(lon)s - loc.rad_lon) / 2), 2)
                    )
                )
            )
            <= %(distance)s
        """ % {"r": r, "distance": distance, "lat": lat, "lon": lon}
        return self.__execute__(query)

    def locations_within_straight_line(self, distance, x, y, z):
        query = """
        SELECT *
        FROM locations loc
        WHERE
            sqrt(
                pow(%(x)s - x, 2) +
                pow(%(y)s - y, 2) +
                pow(%(z)s - z, 2)
            )
            <= %(distance)s
        """ % {"r": r, "distance": distance, "x": x, "y": y, "z": z}
        return self.__execute__(query)

    def locations_within_earthdist(self, distance, lat, lon):
        query = """
        SELECT *
        FROM locations loc
        WHERE
            earth_box( ll_to_earth( %(lat)s, %(lon)s ), %(distance)s ) @> ll_to_earth(loc.lat, loc.lon);
        """ % {"distance": distance / 0.00062137, "lat": lat, "lon": lon}
        return self.__execute__(query)

    def __execute__(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()


    def __del__(self):
        if self.con:
            self.con.close()
