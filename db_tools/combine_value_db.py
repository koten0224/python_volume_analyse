# -*- coding: utf-8 -*-

import sqlite3 as sql

if __name__=='__main__':

    db = sql.connect('tech.db')
    cursor = db.cursor()
    cursor.execute("select val from variable where name='total_amount'")
    result=cursor.fetchone()[0]
    db.close()
    input(result)
    
    db = sql.connect('test.db')
    cursor = db.cursor()
    cursor.execute("select val from variable where name='total_amount'")
    result+=cursor.fetchone()[0]
    cursor.execute("update variable set val={} where name='total_amount'".format(result))
    db.commit()
    db.close()
    input()


