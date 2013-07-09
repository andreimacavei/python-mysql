import unittest
import sqlite3
from conn_mysqldb.py import *

def setup():
    conn = sqlite3.connect('example.db')
    curs = conn.cursor()
    
    # Create table
    curs.execute('''CREATE TABLE details (
                 id int,
                 name text,
                 telephone text,
                 date date
                 )''')

    # Copy the producer database into a temporary database for testing purpose
    sql = "SELECT * FROM details"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        curs.execute("INSERT INTO details VALUES(?, ?, ?, ?)" % (
                     row[0], row[1], row[2], row[3]
                     ))
        
    conn.commit()

# Initial setup
setup()

def conn_to_db()
    conn = sqlite3.connect('example.db')
    curs = conn.cursor()

def test_that_a_record_was_inserted()
    conn_to_db()
    
