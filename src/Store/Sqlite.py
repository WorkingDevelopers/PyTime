"""
Created on Nov 11, 2012

@author: Christoph Graupner <ch.graupner@workingdeveloper.de>
"""
import sqlite3 as lite
import os
import time

class Sqlite(object):
    """
    classdocs
    """

    def __init__(self, dbfile):
        """
        Constructor
        """
        self._file = dbfile
        self._db = None

    def __del__(self):
        self.close()

    def write(self, aTime, event, reason=None):
        if reason is not None:
            logInsert = "INSERT INTO logonoff (time,event,timezone,reason) VALUES ('" + time.strftime("%Y%m%dT%H%M%S",
                aTime) + "','" + event + "','" + str(time.timezone / 3600) + "','" + reason + "');"
        else:
            logInsert = "INSERT INTO logonoff (time,event,timezone) VALUES ('" + time.strftime("%Y%m%dT%H%M%S",
                aTime) + "','" + event + "','" + str(time.timezone / 3600) + "');"
        cur = self.getDb().cursor()
        cur.execute(logInsert)
        self.getDb().commit()

    def getDb(self):
        if self._db is None:
            self.connect()
        return self._db

    def createDB(self, db):
        with db:
            cur = db.cursor()
            cur.execute("""
            CREATE TABLE logonoff(
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "time" DATETIME NOT NULL,
                "event" VARCHAR(50) NOT NULL,
                "timezone" SMALLINT NOT NULL DEFAULT -1,
                "reason" VARCHAR(255) NULL
                )
            """)

    def connect(self):
        if not os.path.exists(self._file):
            self._db = lite.connect(self._file)
            self.createDB(self._db)
        else:
            self._db = lite.connect(self._file)

    def close(self):
        if self._db is not None:
            self._db.close()
