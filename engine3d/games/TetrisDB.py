from pysqlite2 import dbapi2 as sqlite
import os

class TetrisDB:
    def __init__(self,db):
            self.create = 1
            if os.path.exists(db):
                self.create = 0
                
            self.connection = sqlite.connect(db)
            self.cursor = self.connection.cursor()
            
            if self.create:
                self.createDB()
            
    def addScore(self,name,score):
        self.cursor.execute('INSERT INTO score VALUES (null, ?, ?)',(name, score))
        self.connection.commit()
        
    def getToTen(self):
        self.cursor.execute('SELECT name,score,id FROM score order by score desc, id desc limit 0,10')
        return self.cursor.fetchall()
    
    def getNewestId(self):
        self.cursor.execute('SELECT id FROM score order by id desc limit 0,1')
        try:
            return self.cursor.fetchall()[0][0]
        except: # no scores are on reccord
            return -1
        
    def clearScore(self):
        self.cursor.execute('Delete from score')
        self.connection.commit()
        
    def createDB(self):
        self.cursor.execute('CREATE TABLE score (id INTEGER PRIMARY KEY,name VARCHAR(255), score INT(11))')
        self.connection.commit()