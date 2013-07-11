import unittest
import sqlite3
from conn_mysqldb.py import *

class TestMySQLdbConnFunctions(unittest.TestCase):

    def setup():
        conn = sqlite3.connect(:memory:, 'example.db')
        curs = conn.cursor()
        
        # Create table
        curs.execute('''CREATE TABLE details (
                     id int,
                     name text,
                     telephone text,
                     date text
                     )''')

    def conn_to_db()
        conn = sqlite3.connect('example.db')
        curs = conn.cursor()

    def disconnect()
        curs.close()    

    #class ConnMsqldbTestSuite(unittest.TestCase):

    def test_that_a_record_was_inserted()

        name = 'Andrei'
        telephone = '0737037718'
        

