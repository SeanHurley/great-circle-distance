import psycopg2
import sys
import re
import datetime

r = 3959
class Psql:
    def __init__(self):
        self.con = psycopg2.connect(database='geo', user='seanhurley', host="/tmp")
        self.cur = self.con.cursor()

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
        self.cur.execute(query)
        return self.cur.fetchall()

    def __del__(self):
        if self.con:
            self.con.close()
