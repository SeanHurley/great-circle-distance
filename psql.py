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

    def __del__(self):
        if self.con:
            self.con.close()