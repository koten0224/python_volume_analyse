# -*- coding: utf-8 -*-
import sqlite3 as sql

if __name__=='__main__':

    db = sql.connect('tech.db')
    cursor = db.cursor()
    cursor.execute('select * from urls')
    result=cursor.fetchall()
    db.close()
    
    db = sql.connect('test.db')
    cursor = db.cursor()
    for i in set(result):
        cursor.execute('insert into urls values {}'.format(i))
    db.commit()
    db.close()


