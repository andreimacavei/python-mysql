import unittest
import sqlite3
from conn_msqldb import *

class TestMySQLdbConnFunctions(unittest.TestCase):

    def setUp(self):
        db  = sqlite3.connect('example.db')
        self.curs = db.cursor()
        self.test_table = 'testdb'

        # Create table
        """self.curs.execute('''CREATE TABLE testdb (
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     telephone TEXT,
                     date DATETIME DEFAULT CURRENT_TIMESTAMP
                     )''')"""
    def tearDown(self):
        self.curs.close()    

    def test_insert_record(self):
        # define input
        name = 'Andrei'
        telephone = '0737037718'
        date = datetime.now()
        
        # apply transformation
        insert_record(self.test_table, name, telephone)

        last_id = self.curs.lastrowid
        results = self.curs.execute('SELECT * FROM %s WHERE id = %s' % (test_table, last_id))
        print results
        # assert

    def test_update_record(self):
        # define input
        name = 'Andrei'
        telephone = '0723474474'
        name_new = 'Andrei Gabriel'
        telephone_new = '0737321443'

        # apply transformation
        



unittest.main()
#suite = unittest.TestLoader().loadTestsFromTestCase(TestMySQLdbConnFunctions)
#unittest.TextTestRunner(verbosity=2).run(suite)

