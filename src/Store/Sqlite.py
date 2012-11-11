'''
Created on Nov 11, 2012

@author: Christoph Graupner
'''
import sqlite3 as lite
import os
import time

class Sqlite(object):
    '''
    classdocs
    '''

    def __init__(self,dbfile):
        '''
        Constructor
        '''
        self._file = dbfile
        self._db = None
        
    def __del__(self):
        self.close()
        
    def write(self,aTime,event):
        logInsert = "INSERT INTO logonoff (time,event) VALUES ('"+time.strftime("%Y%m%dT%H%M%S",aTime)+"','"+event+"');"
        cur = self.getDb().cursor()
        cur.execute(logInsert)
        self.getDb().commit()
    
    def getDb(self):
        if self._db == None:
            self.connect()
        return self._db
    
    def createDB(self,db):
        with db:
            cur = db.cursor()    
            cur.execute("""
            CREATE TABLE logonoff(
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "time" DATETIME NOT NULL,
                "event" VARCHAR(50) NOT NULL)
            """)
    
    def connect(self):
        if not os.path.exists(self._file):
            self._db = lite.connect(self._file)
            self.createDB(self._db)
        else:
            self._db = lite.connect(self._file)
    
    def close(self):
        if self._db != None:
            self._db.close()
